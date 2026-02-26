from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):
    ui_color = '#80BD9E'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="redshift",
                 table="",
                 sql_query="",
                 append_only=False, # Standard naming for this toggle
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.sql_query = sql_query
        self.append_only = append_only

    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        if not self.append_only: 
            self.log.info(f"Truncating (clearing) dimension table: {self.table}")
            redshift.run(f"DELETE FROM {self.table}")
        
        self.log.info(f"Loading data into dimension table: {self.table}")
        load_sql = f"INSERT INTO {self.table} {self.sql_query}"
        redshift.run(load_sql)
        
        self.log.info(f"Successfully loaded {self.table}")