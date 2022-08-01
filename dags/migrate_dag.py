from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.hooks.mysql_hook import MySqlHook
from airflow.operators.dummy import DummyOperator
from airflow.providers.mysql.operators.mysql import MySqlOperator
from datetime import datetime, timedelta


def migrate_to_mysql():
    pg_hook = PostgresHook(postgres_conn_id="postgres_localhost")
    mysql_hook = MySqlHook(mysql_conn_id="mysql_localhost")
    conn = mysql_hook.get_sqlalchemy_engine()
    df = pg_hook.get_pandas_df(sql="SELECT * FROM traffic_flow;")

    df.to_sql(
        "open_traffic",
        con=conn,
        if_exists="replace",
        index=False,
    )


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['diyye101@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    "start_date": datetime(2022, 7, 20, 2, 30, 00),
    'retry_delay': timedelta(minutes=5)
}

with DAG(
        "migration_dag",
        default_args=default_args,
        schedule_interval="0 * * * *",
        catchup=False,
) as dag:
    migrate_op = PythonOperator(
        task_id="load_data",
        python_callable=migrate_to_mysql
    )

migrate_op
