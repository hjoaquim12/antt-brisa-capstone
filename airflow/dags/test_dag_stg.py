"""Test DAG.

A dag with a single task to test a BashOperator running a dbt command.
"""

from __future__ import annotations

import sys
from datetime import datetime

from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import dag

# The ingest module lives at /opt/airflow/ingest inside the container; make
# sure it is importable regardless of how Airflow launches the worker.
INGEST_DIR = "/opt/airflow/ingest"
if INGEST_DIR not in sys.path:
    sys.path.insert(0, INGEST_DIR)


@dag(
    dag_id="test_dbt_dag",
    description="Test DAG for running dbt commands.",
    schedule="@monthly",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    max_active_runs=1,
    tags=["capstone", "test", "dbt"],
)
def test_dbt_command():

    _ = BashOperator(
        task_id="dbt_run",
        bash_command=(
            "dbt run --select stg_toll_traffic "
            "--project-dir /opt/airflow/dbt_project "
            "--profiles-dir /opt/airflow/dbt_project"
        ),
    )


test_dbt_command()
