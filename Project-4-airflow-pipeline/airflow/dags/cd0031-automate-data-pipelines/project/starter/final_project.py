from datetime import datetime, timedelta
from airflow.decorators import dag
from airflow.operators.dummy_operator import DummyOperator

from final_project_operators.stage_redshift import StageToRedshiftOperator
from final_project_operators.load_fact import LoadFactOperator
from final_project_operators.load_dimension import LoadDimensionOperator
from final_project_operators.data_quality import DataQualityOperator

from udacity.common.final_project_sql_statements import SqlQueries


default_args = {
    'owner': 'udacity',
    'start_date': datetime(2026, 1, 1),
    'depends_on_past': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'catchup': False,
    'email_on_retry': False
}


@dag(
    default_args=default_args,
    description='Load and transform data in Redshift with Airflow',
    schedule_interval='@hourly'
)
def final_project():

    start_operator = DummyOperator(task_id='Begin_execution')

    # -------------------------
    # STAGING TASKS
    # -------------------------
    stage_events_to_redshift = StageToRedshiftOperator(
        task_id='Stage_events',
        redshift_conn_id="redshift",
        aws_credentials_id="aws_credentials",
        table="staging_events",         
        s3_bucket="han-udacity-project",
        s3_key="log-data",
        json_path="s3://han-udacity-project/log_json_path.json",
        region="us-east-1"
    )

    stage_songs_to_redshift = StageToRedshiftOperator(
            task_id='Stage_songs',
            redshift_conn_id="redshift",
            aws_credentials_id="aws_credentials",
            table="staging_songs",                 
            s3_bucket="han-udacity-project",        
            s3_key="song-data",
            json_path="auto",
            region="us-east-1"
        )

    # -------------------------
    # FACT TABLE LOAD
    # -------------------------

    load_songplays_table = LoadFactOperator(
        task_id='Load_songplays_fact_table',
        redshift_conn_id="redshift",
        table="songplays",                    
        sql_query=SqlQueries.songplay_table_insert 
    )


    # -------------------------
    # DIMENSION LOADS
    # (delete-load pattern: append_only=False)
    # -------------------------

    load_user_dimension_table = LoadDimensionOperator(
        task_id='Load_user_dim_table',
        redshift_conn_id="redshift",
        table="users", 
        sql_query=SqlQueries.user_table_insert,
        append_only=False
    )

    load_song_dimension_table = LoadDimensionOperator(
        task_id='Load_song_dim_table',
        redshift_conn_id="redshift",
        table="songs", 
        sql_query=SqlQueries.song_table_insert,
        append_only=False
    )

    load_artist_dimension_table = LoadDimensionOperator(
        task_id='Load_artist_dim_table',
        redshift_conn_id="redshift",
        table="artists", 
        sql_query=SqlQueries.artist_table_insert,
        append_only=False
    )

    load_time_dimension_table = LoadDimensionOperator(
        task_id='Load_time_dim_table',
        redshift_conn_id="redshift",
        table="time", 
        sql_query=SqlQueries.time_table_insert,
        append_only=False
    )

    # -------------------------
    # DATA QUALITY CHECKS
    # -------------------------

    run_quality_checks = DataQualityOperator(
        task_id='Run_data_quality_checks',
        redshift_conn_id="redshift",
        dq_checks=[ 
            {"check_sql": "SELECT COUNT(*) FROM songplays WHERE songplay_id IS NULL", "expected_result": 0},
            {"check_sql": "SELECT COUNT(*) FROM users WHERE userid IS NULL", "expected_result": 0}
        ]
    )

    end_operator = DummyOperator(task_id='Stop_execution')

    # -------------------------
    # DAG DEPENDENCIES
    # -------------------------

    start_operator >> [stage_events_to_redshift, stage_songs_to_redshift]

    [stage_events_to_redshift, stage_songs_to_redshift] >> load_songplays_table

    load_songplays_table >> [
        load_user_dimension_table,
        load_song_dimension_table,
        load_artist_dimension_table,
        load_time_dimension_table
    ]

    [
        load_user_dimension_table,
        load_song_dimension_table,
        load_artist_dimension_table,
        load_time_dimension_table
    ] >> run_quality_checks

    run_quality_checks >> end_operator


final_project_dag = final_project()