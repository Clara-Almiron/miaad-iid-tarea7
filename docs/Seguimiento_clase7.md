# Seguimiento clase 7

Proyecto evaluado: `fpuna-maven`

## Estado general

Avance actual: 3 de 5 puntos del entregable completos, 1 parcialmente resuelto y 1 pendiente.
Segun la clase 7, el objetivo es cerrar el pipeline completo `MySQL -> Airbyte -> MotherDuck -> dbt -> Prefect -> Metabase`, con evidencia de ejecucion y visualizacion final.

## Checklist del entregable

- [x] Airbyte: Connection MySQL -> MotherDuck funcionando
  Evidencia actual:
  - la arquitectura del proyecto contempla Airbyte en `README.md`
  - el pipeline de Prefect usa `AIRBYTE_CONNECTION_ID` y llamadas a la API de Airbyte en `prefect/ecommerce_pipeline.py`
  - existe `.env.example` con variables `AIRBYTE_*`
  - captura agregada en `docs/Connection_MySQL_to_MotherDuck.PNG`

- [x] dbt: Modelos en `main_staging` y `main_marts` ejecutándose
  Evidencia:
  - modelos `staging` y `marts` presentes en `dbt/models/`
  - artefactos en `dbt/target/` (`manifest.json`, `catalog.json`, `run_results.json`, `index.html`)
  - `run_results.json` muestra resultados exitosos sobre modelos en `maven_fuzzy_staging` y `maven_fuzzy_marts`
  Observacion: los ajustes recientes en `stg_order_items.sql` y `stg_sessions.sql` corrigen flags booleanos codificados como strings.

- [ ] Prefect: Pipeline completo con archivo `.env` configurado
  Estado: parcial.
  Evidencia actual:
  - pipeline completo implementado en `prefect/ecommerce_pipeline.py`
  - carga de variables de entorno con `dotenv`
  - `.env.example` presente en la raiz
  Faltante: no se observa un archivo `.env` versionado en la raiz del proyecto ni captura de ejecucion exitosa en Prefect UI.

- [ ] Metabase: Dashboard con al menos 5 visualizaciones y 2 filtros
  Estado: pendiente o no evidenciado.
  Evidencia actual:
  - configuracion de Metabase en `docker/docker-compose.yml`
  - `Dockerfile` y configuracion del entorno Docker disponibles
  Faltante: no hay consultas SQL guardadas, capturas de dashboard, ni evidencia visible de 5 visualizaciones y 2 filtros.

- [ ] Capturas: Prefect UI mostrando ejecución exitosa + Dashboard
  Estado: pendiente.
  Evidencia actual:
  - existen varias capturas de DAG de dbt en `docs/`
  Faltante:
  - captura de Prefect UI con una corrida exitosa
  - captura del dashboard final de Metabase

## Trabajo ya realizado

- Se estructuro el proyecto completo con las capas esperadas del pipeline.
- Se configuro entorno Docker para MySQL, phpMyAdmin y Metabase en `docker/docker-compose.yml`.
- Se documento la conexion Airbyte -> MotherDuck con la captura `docs/Connection_MySQL_to_MotherDuck.PNG`.
- Se creo un `dbt` project funcional con fuentes, staging y marts.
- Se ajustaron modelos de `staging` para normalizar banderas booleanas problemáticas (`is_primary_item`, `is_repeat_session`).
- Se ejecutaron tests de dbt y se generaron artefactos de documentacion en `dbt/target/`.
- Se implemento un pipeline de Prefect con tareas para:
  - disparar Airbyte via API
  - ejecutar `dbt deps`
  - ejecutar `dbt run`
  - ejecutar `dbt test`
  - generar docs

## Pendientes prioritarios

1. Crear el archivo `.env` real para Prefect en la raiz del proyecto y validar la carga de variables.
2. Ejecutar el flujo de Prefect y guardar una captura de la UI con una corrida exitosa.
3. Levantar Metabase, conectar a MotherDuck y construir un dashboard con al menos 5 visualizaciones y 2 filtros.
4. Guardar una captura del dashboard final en `docs/`.

## Propuesta de implementación

1. Verificar MySQL y datos cargados con Docker:
   ```bash
   cd docker
   docker compose up -d
   ```
2. Configurar o verificar Airbyte:
   - source MySQL apuntando a `maven_fuzzy_factory`
   - destination MotherDuck apuntando a `airbyte_curso`
   - sync de las 6 tablas
3. Crear `.env` a partir de `.env.example` y completar:
   - `MOTHERDUCK_TOKEN`
   - `AIRBYTE_CONNECTION_ID`
   - `AIRBYTE_HOST`
   - `AIRBYTE_PORT`
   - `AIRBYTE_USERNAME`
   - `AIRBYTE_PASSWORD`
4. Ejecutar Prefect:
   ```bash
   prefect server start
   cd prefect
   python ecommerce_pipeline.py
   ```
5. Validar dbt:
   ```bash
   cd dbt
   dbt run
   dbt test
   dbt docs generate
   ```
6. Levantar Metabase y crear dashboard:
   ```bash
   cd docker
   docker compose up -d metabase
   ```
7. Generar y guardar capturas finales:
   - Prefect UI con corrida exitosa
   - Dashboard de Metabase con visualizaciones y filtros

## Nota

Este seguimiento se construyo a partir de `docs/Entregable_clase7.txt`, del PDF `docs/clase7.pdf` y del estado actual del repositorio. El proyecto ya tiene base tecnica fuerte en `dbt` y `Prefect`, pero todavia falta evidencia final de Airbyte y Metabase para cerrar completamente el entregable.
