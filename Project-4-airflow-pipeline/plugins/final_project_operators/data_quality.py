from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):
    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="redshift",
                 dq_checks=[], # List of dicts like {'check_sql': '...', 'expected_result': 0}
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.dq_checks = dq_checks

    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        # Iterate through the provided list of checks
        for check in self.dq_checks:
            sql = check.get('check_sql')
            expected = check.get('expected_result')

            self.log.info(f"Running data quality check: {sql}")
            
            # Execute the test and get results
            records = redshift.get_records(sql)
            
            # Standard developer check: verify the query actually returned data
            if len(records) < 1 or len(records[0]) < 1:
                raise ValueError(f"Data quality check failed. Query returned no results: {sql}")

            # Extract the actual value and compare to the expected result
            actual = records[0][0]
            if actual != expected:
                raise ValueError(f"Data quality check failed. Expected {expected}, but got {actual}")
            
            self.log.info(f"Check PASSED: {actual} matches expected {expected}")
            
        self.log.info("All data quality checks passed successfully!")