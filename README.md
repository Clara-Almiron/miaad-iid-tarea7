# Maven Fuzzy Factory ELT Pipeline

Pipeline de datos para el ecommerce Maven Fuzzy Factory.

## Arquitectura

```
MySQL (Source) → Airbyte → MotherDuck (DWH) → dbt (Transform) → Metabase (BI)
```

## Setup

### 1. Instalar dependencias

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configurar variables de entorno

```bash
cp .env.example .env
# Editar .env con tus credenciales
```

### 3. Configurar dbt profile

Crear/editar `~/.dbt/profiles.yml`:

```yaml
maven_fuzzy_factory:
  outputs:
    dev:
      type: duckdb
      path: "md:maven_fuzzy_factory"
      motherduck_token: "{{ env_var('MOTHERDUCK_TOKEN') }}"
  target: dev
```

### 4. Verificar conexión dbt

```bash
cd dbt
dbt debug
```

### 5. Instalar paquetes dbt

```bash
dbt deps
```

## Uso

### Ejecutar dbt manualmente

```bash
cd dbt

# Ejecutar todos los modelos
dbt run

# Ejecutar solo staging
dbt run --select staging

# Ejecutar solo marts
dbt run --select marts

# Ejecutar tests
dbt test

# Generar documentación
dbt docs generate
dbt docs serve
```

### Ejecutar pipeline completo con Prefect

```bash
cd prefect
python ecommerce_pipeline.py
```

### Programar ejecución automática

El pipeline está configurado para ejecutarse diariamente a las 6am.

Para iniciar el servidor de Prefect:

```bash
prefect server start
```

## Modelos dbt

### Staging (views)

| Modelo | Descripción |
|--------|-------------|
| `stg_sessions` | Sesiones web limpias (~450K registros) |
| `stg_pageviews` | Pageviews (~1.1M registros) |
| `stg_orders` | Órdenes con margen calculado (~32K registros) |
| `stg_order_items` | Items con nombre de producto (~54K registros) |
| `stg_refunds` | Reembolsos (~800 registros) |

### Marts (tables)

| Modelo | Descripción |
|--------|-------------|
| `fct_daily_sales` | Métricas diarias (sessions, orders, revenue, conversion) |
| `fct_channel_performance` | Performance por canal/campaña |
| `fct_product_performance` | Performance por producto |
| `obt_orders_enriched` | One Big Table con todo el contexto de cada orden |

## Métricas de Negocio

- **Conversion Rate**: `orders / sessions * 100`
- **Margin**: `price_usd - cogs_usd`
- **AOV (Average Order Value)**: `revenue / orders`
- **Revenue per Session**: `revenue / sessions`
- **Refund Rate**: `refunds / units_sold * 100`
