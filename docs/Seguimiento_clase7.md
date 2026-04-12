# Seguimiento clase 7

Proyecto evaluado: `fpuna-maven`

## Estado general

Avance actual: 5 de 5 puntos completos.

Objetivo de la clase: cerrar el pipeline completo `MySQL -> Airbyte -> MotherDuck -> dbt -> Prefect -> Metabase`, con evidencia de ejecucion y visualizacion final.

## Checklist del entregable

- [x] Airbyte: Connection MySQL -> MotherDuck funcionando
  Evidencia actual:
  - captura agregada en `docs/Connection_MySQL_to_MotherDuck.PNG`
  - el pipeline de Prefect usa `AIRBYTE_CONNECTION_ID` y llamadas a la API de Airbyte en `prefect/ecommerce_pipeline.py`
  - existe `.env.example` con variables `AIRBYTE_*`

- [x] dbt: Modelos en `main_staging` y `main_marts` ejecutandose
  Evidencia actual:
  - modelos en `dbt/models/staging/` y `dbt/models/marts/`
  - ejecucion exitosa de `dbt run` y `dbt test`
  - resultado final de tests: `PASS=20 WARN=0 ERROR=0 SKIP=0 TOTAL=20`
  - artefactos generados en `dbt/target/`: `manifest.json`, `catalog.json`, `run_results.json`, `index.html`
  - capturas DAG disponibles en `docs/`
  Observacion: se corrigieron en `staging` las banderas `is_primary_item` e `is_repeat_session`, que llegaban codificadas como strings.

- [x] Prefect: Pipeline completo con archivo `.env` configurado
  Evidencia actual:
  - flujo implementado en `prefect/ecommerce_pipeline.py`
  - carga de variables con `dotenv`
  - archivo `.env.example` presente en la raiz
  - archivo `.env` configurado localmente en `prefect/`
  - captura de corrida exitosa en `docs/prefect_ejecucion_exitosa.PNG`

- [x] Metabase: Dashboard con al menos 5 visualizaciones y 2 filtros
  Evidencia actual:
  - configuracion Docker en `docker/docker-compose.yml`
  - archivo `docker/Dockerfile`
  - dashboard construido y capturado en `docs/Dashboard.PNG`

- [x] Capturas: Prefect UI mostrando ejecucion exitosa + Dashboard
  Evidencia disponible:
  - capturas de DAG dbt en `docs/`
  - captura de Airbyte en `docs/Connection_MySQL_to_MotherDuck.PNG`
  - captura de Prefect UI en `docs/prefect_ejecucion_exitosa.PNG`
  - captura del dashboard final en `docs/Dashboard.PNG`

## Trabajo ya realizado

- Se estructuro el proyecto con las capas esperadas del pipeline.
- Se dejo configurado Docker para MySQL, phpMyAdmin y Metabase.
- Se documento la conexion Airbyte -> MotherDuck con la captura `docs/Connection_MySQL_to_MotherDuck.PNG`.
- Se construyo el proyecto dbt con modelos `staging` y `marts`.
- Se corrigieron transformaciones en `stg_order_items.sql` y `stg_sessions.sql` para normalizar flags booleanos.
- Se ejecutaron `dbt run`, `dbt test` y `dbt docs generate` exitosamente.
- Se generaron artefactos y capturas DAG para modelos y tests.
- Se implemento el flujo de Prefect para orquestar Airbyte + dbt.
- Se ejecuto Prefect y se guardo evidencia de ejecucion exitosa.
- Se construyo el dashboard de Metabase y se guardo evidencia en `docs/Dashboard.PNG`.

## Nota

Este seguimiento se construyo a partir de `docs/Entregable_clase7.txt`, `docs/clase7.pdf` y el estado actual del repositorio. El entregable ya cuenta con evidencia para Airbyte, dbt, Prefect, Metabase y capturas finales.
