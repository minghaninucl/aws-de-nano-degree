from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadFactOperator(BaseOperator):
    ui_color = '#F98866'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="redshift",
                 table="",
                 sql_query="",
                 *args, **kwargs):

        super(LoadFactOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.sql_query = sql_query

    def execute(self, context):
        # Setting up the connection using the PostgresHook
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        self.log.info(f"Preparing to load data into the {self.table} fact table")
        
        # Building the SQL dynamically. Fact tables are massive and 
        # should only allow append functionality, so no truncate here.
        insert_sql = f"INSERT INTO {self.table} {self.sql_query}"
        
        self.log.info(f"Executing load query for {self.table}")
        redshift.run(insert_sql)
        
        self.log.info(f"Successfully loaded fact table: {self.table}")