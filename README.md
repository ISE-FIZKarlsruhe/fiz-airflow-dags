# Airflow DAGs (FIZ)

This repository contains Apache Airflow DAGs used in our Airflow deployment.

## Where to add a DAG

Put all DAG Python files under:

- `dags/` for production DAGs
- `dags/demo/` for demo / example DAGs

Airflow scans the `dags/` directory recursively, so subfolders are fine.

### Minimal requirements

- DAG ID: must be **unique** across all DAGs
- The file must end in `.py`
- No missing Python dependencies (otherwise it will show up under **Import Errors**)

## How to add a new DAG (step-by-step)

1. Create a new Python file in:
   - `dags/<your_dag>.py` (production)

2. Define your DAG with a unique `dag_id`.

3. Ensure the DAG is instantiated, for example:
   ```python
   dag = my_dag()
   ```
   or
   ```python
   my_dag()
   ```

4. Commit and push your changes.

5. **Update this README**:
   - Add your DAG to the **Available DAGs** table below
   - Keep the table sorted by directory then DAG ID

## Available DAGs

| DAG ID | Directory | Description |
|---|---|---|
| `ontology_iri_monitor` | `dags/IRIstatus.py` | Monitors configured ontology IRIs by requesting multiple RDF content types, parses RDF, extracts `owl:versionIRI` / `owl:priorVersion`, and writes latest-only results to the results DB table `ontology_results` plus a Superset-friendly summary view `ontology_iri_latest_summary`. |
| `demo1` | `dags/demo/demo1.py` | Simple demo DAG: runs a `BashOperator` and then a Python task printing a message. |
| `demo2` | `dags/demo/demo2.py` | Demo DAG using HITL operators: collects form input, branches on user selection, and runs one of two Bash tasks. |
