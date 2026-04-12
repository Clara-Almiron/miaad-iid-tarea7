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

## Pendientes prioritarios

1. Revisar que las capturas finales se vean correctamente en el informe o entrega.
2. Hacer commit final del proyecto.

## Paso a paso para terminar el trabajo

### 1. Verificar evidencias generadas

1. Confirmar que existen las capturas obligatorias:
   - `docs/Connection_MySQL_to_MotherDuck.PNG`
   - `docs/prefect_ejecucion_exitosa.PNG`
   - `docs/Dashboard.PNG`
2. Abrir las capturas y verificar que muestran claramente:
   - conexion Airbyte MySQL -> MotherDuck
   - corrida exitosa de Prefect
   - dashboard de Metabase con visualizaciones y filtros

### 2. Revalidar dbt si se necesita una evidencia actualizada

1. Desde el proyecto dbt:
   ```bash
   cd /home/clara/dbt_duckdb/fpuna-maven/dbt
   source /home/clara/dbt_duckdb/motherduck_env.sh
   source /home/clara/dbt_duckdb/dbt-env/bin/activate
   dbt run
   dbt test
   dbt docs generate
   ```
2. La ultima evidencia registrada para tests fue exitosa: `PASS=20 WARN=0 ERROR=0 SKIP=0 TOTAL=20`.

### 3. Revisar Prefect

1. Si se necesita regenerar la evidencia:
   ```bash
   prefect server start
   ```
2. En otra terminal, ejecutar el pipeline:
   ```bash
   cd /home/clara/dbt_duckdb/fpuna-maven/prefect
   python ecommerce_pipeline.py
   ```
3. Abrir `http://localhost:4200`.
4. Verificar que exista una corrida `Completed`.
5. La evidencia actual ya quedo guardada como `docs/prefect_ejecucion_exitosa.PNG`.

### 4. Revisar Metabase

1. Entrar a `http://localhost:3000`.
2. Confirmar que el dashboard final conserva:
   - al menos 5 visualizaciones
   - al menos 2 filtros
   - conexion a MotherDuck
3. La evidencia actual ya quedo guardada como `docs/Dashboard.PNG`.

### 5. Cierre del entregable

1. Revisar el estado del repo:
   ```bash
   git -C /home/clara/dbt_duckdb/fpuna-maven status
   ```
2. Hacer el commit final.

## Nota

Este seguimiento se construyo a partir de `docs/Entregable_clase7.txt`, `docs/clase7.pdf` y el estado actual del repositorio. El entregable ya cuenta con evidencia para Airbyte, dbt, Prefect, Metabase y capturas finales.
