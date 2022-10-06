from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.subdag import SubDagOperator
from sub_dags.subdag_downloads import subdag_downloads
from sub_dags.subdag_transforms import subdag_transform

from datetime import datetime

with DAG(
    "group_dag",
    start_date=datetime(2022, 1, 1),
    schedule_interval="@daily",
    catchup=False,
) as dag:

    args = {
        "start_date": dag.start_date,
        "schedule_interval": dag.schedule_interval,
        "catchup": dag.catchup,
    }

    downloads = SubDagOperator(
        task_id='downloads', 
        subdag=subdag_downloads(dag.dag_id, 'downloads', args))

    check_files = BashOperator(
        task_id="check_files", 
        bash_command="sleep 10")

    transform = SubDagOperator(task_id = 'transform',
        subdag=subdag_transform(dag.dag_id, 'transform', args))

    (
        downloads >> check_files >> transform
    )
