from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.hooks.mysql_hook import MySqlHook
from airflow.operators.dummy import DummyOperator
from airflow.providers.mysql.operators.mysql import MySqlOperator
from datetime import datetime, timedelta

pg_hook = PostgresHook(postgres_conn_id="postgres_localhost")
mysql_hook = MySqlHook(mysql_conn_id="mysql_localhost")
conn = mysql_hook.get_sqlalchemy_engine()


def migrate_to_mysql():
    df = pg_hook.get_pandas_df(sql="SELECT * FROM open_traffic;")
    df.to_sql(
        "open_traffic",
        con=conn,
        if_exists="replace",
        index=False,
    )


def migrate_dbt_to_mysql():
    df_open_traffic_all = pg_hook.get_pandas_df(sql="SELECT * FROM open_traffic_all;")
    df_open_traffic_all.to_sql(
        "open_traffic_all",
        con=conn,
        if_exists="replace",
        index=False,
    )
    df_speed_above = pg_hook.get_pandas_df(sql="SELECT * FROM speed_above;")
    df_speed_above.to_sql(
        "speed_above",
        con=conn,
        if_exists="replace",
        index=False,
    )
    df_speed_below = pg_hook.get_pandas_df(sql="SELECT * FROM speed_below;")
    df_speed_below.to_sql(
        "speed_below",
        con=conn,
        if_exists="replace",
        index=False,
    )
    df_type_bus = pg_hook.get_pandas_df(sql="SELECT * FROM type_bus;")
    df_type_bus.to_sql(
        "type_bus",
        con=conn,
        if_exists="replace",
        index=False,
    )
    df_type_car = pg_hook.get_pandas_df(sql="SELECT * FROM type_car;")
    df_type_car.to_sql(
        "type_car",
        con=conn,
        if_exists="replace",
        index=False,
    )
    df_type_heavy_vehicle = pg_hook.get_pandas_df(sql="SELECT * FROM type_heavy_vehicle;")
    df_type_heavy_vehicle.to_sql(
        "type_heavy_vehicle",
        con=conn,
        if_exists="replace",
        index=False,
    )
    df_type_medium_vehicle = pg_hook.get_pandas_df(sql="SELECT * FROM type_medium_vehicle;")
    df_type_medium_vehicle.to_sql(
        "type_medium_vehicle",
        con=conn,
        if_exists="replace",
        index=False,
    )
    df_type_motorcycle = pg_hook.get_pandas_df(sql="SELECT * FROM type_motorcycle;")
    df_type_motorcycle.to_sql(
        "type_motorcycle",
        con=conn,
        if_exists="replace",
        index=False,
    )
    df_type_taxi = pg_hook.get_pandas_df(sql="SELECT * FROM type_taxi;")
    df_type_taxi.to_sql(
        "type_taxi",
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
    migrate_all_data_op = PythonOperator(
        task_id="migrate_data",
        python_callable=migrate_to_mysql
    )
    migrate_dbt_data_op = PythonOperator(
        task_id="migrate_dbt_data",
        python_callable=migrate_dbt_to_mysql
    )

migrate_all_data_op >> migrate_dbt_data_op
