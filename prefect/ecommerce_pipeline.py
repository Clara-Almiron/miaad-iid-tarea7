"""
Pipeline ELT para Maven Fuzzy Factory
MySQL -> Airbyte -> MotherDuck -> dbt
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from prefect import flow, task, get_run_logger
from prefect_airbyte.server import AirbyteServer
from prefect_airbyte.connections import AirbyteConnection
from prefect_airbyte.flows import run_connection_sync
from prefect_dbt.cli.commands import DbtCoreOperation

# Cargar variables de entorno
load_dotenv()

# Configuración
AIRBYTE_HOST = os.getenv("AIRBYTE_HOST", "localhost")
AIRBYTE_PORT = int(os.getenv("AIRBYTE_PORT", 8000))
AIRBYTE_CONNECTION_ID = os.getenv("AIRBYTE_CONNECTION_ID")
DBT_PROJECT_DIR = Path(__file__).parent.parent / "dbt"
DBT_PROFILES_DIR = Path.home() / ".dbt"


@task(name="Extract and Load with Airbyte", retries=2, retry_delay_seconds=60)
def extract_and_load():
    """Extrae datos de MySQL y carga en MotherDuck via Airbyte"""
    logger = get_run_logger()

    server = AirbyteServer(server_host=AIRBYTE_HOST, server_port=AIRBYTE_PORT)
    connection = AirbyteConnection(
        airbyte_server=server,
        connection_id=AIRBYTE_CONNECTION_ID,
        status_updates=True
    )

    logger.info(f"Iniciando sync de Airbyte para connection {AIRBYTE_CONNECTION_ID}")
    sync_result = run_connection_sync(airbyte_connection=connection)
    logger.info(f"Sync completado. Registros sincronizados: {sync_result.records_synced}")

    return sync_result.records_synced


@task(name="Transform with dbt")
def transform(select: str = None):
    """Ejecuta transformaciones dbt"""
    logger = get_run_logger()

    commands = ["dbt deps"]

    if select:
        commands.append(f"dbt run --select {select}")
    else:
        commands.append("dbt run")

    logger.info(f"Ejecutando dbt en {DBT_PROJECT_DIR}")

    result = DbtCoreOperation(
        commands=commands,
        project_dir=str(DBT_PROJECT_DIR),
        profiles_dir=str(DBT_PROFILES_DIR)
    ).run()

    return result


@task(name="Test with dbt")
def test_data(select: str = None):
    """Ejecuta tests de dbt"""
    logger = get_run_logger()

    if select:
        command = f"dbt test --select {select}"
    else:
        command = "dbt test"

    logger.info(f"Ejecutando tests dbt")

    result = DbtCoreOperation(
        commands=[command],
        project_dir=str(DBT_PROJECT_DIR),
        profiles_dir=str(DBT_PROFILES_DIR)
    ).run()

    return result


@task(name="Generate dbt docs")
def generate_docs():
    """Genera documentación de dbt"""
    result = DbtCoreOperation(
        commands=["dbt docs generate"],
        project_dir=str(DBT_PROJECT_DIR),
        profiles_dir=str(DBT_PROFILES_DIR)
    ).run()

    return result


@flow(name="Ecommerce ELT Pipeline")
def ecommerce_pipeline(
    run_extract: bool = True,
    run_transform: bool = True,
    run_tests: bool = True,
    run_docs: bool = False,
    dbt_select: str = None
):
    """
    Pipeline completo de ELT para Maven Fuzzy Factory

    Args:
        run_extract: Si ejecutar extracción de Airbyte
        run_transform: Si ejecutar transformaciones dbt
        run_tests: Si ejecutar tests de dbt
        run_docs: Si generar documentación
        dbt_select: Selector de modelos dbt (ej: "staging", "marts")
    """
    logger = get_run_logger()
    logger.info("Iniciando pipeline ELT de Maven Fuzzy Factory")

    records_synced = 0

    # 1. Extract & Load
    if run_extract:
        records_synced = extract_and_load()

    # 2. Transform
    if run_transform:
        transform(select=dbt_select)

    # 3. Test
    if run_tests:
        test_data(select=dbt_select)

    # 4. Documentation
    if run_docs:
        generate_docs()

    logger.info("Pipeline completado exitosamente!")

    return {
        "records_synced": records_synced,
        "status": "success"
    }


@flow(name="dbt Only Pipeline")
def dbt_only_pipeline(select: str = None, run_tests: bool = True):
    """Pipeline que solo ejecuta dbt (sin Airbyte)"""
    transform(select=select)
    if run_tests:
        test_data(select=select)


if __name__ == "__main__":
    # Opción 1: Ejecutar una vez
    # ecommerce_pipeline()

    # Opción 2: Ejecutar solo dbt
    # dbt_only_pipeline()

    # Opción 3: Servir con schedule
    ecommerce_pipeline.serve(
        name="ecommerce-daily",
        cron="0 6 * * *",  # Diario a las 6am
        parameters={
            "run_extract": True,
            "run_transform": True,
            "run_tests": True,
            "run_docs": False
        }
    )
