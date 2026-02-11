import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsgluedq.transforms import EvaluateDataQuality
from awsglue import DynamicFrame

def sparkSqlQuery(glueContext, query, mapping, transformation_ctx) -> DynamicFrame:
    for alias, frame in mapping.items():
        frame.toDF().createOrReplaceTempView(alias)
    result = spark.sql(query)
    return DynamicFrame.fromDF(result, glueContext, transformation_ctx)
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Default ruleset used by all target nodes with data quality enabled
DEFAULT_DATA_QUALITY_RULESET = """
    Rules = [
        ColumnCount > 0
    ]
"""

# Script generated for node step_trainer_landing
step_trainer_landing_node1770819907299 = glueContext.create_dynamic_frame.from_catalog(database="stedi-db", table_name="step_trainer_landing", transformation_ctx="step_trainer_landing_node1770819907299")

# Script generated for node customer_curated
customer_curated_node1770818394513 = glueContext.create_dynamic_frame.from_catalog(database="stedi-db", table_name="customer_curated", transformation_ctx="customer_curated_node1770818394513")

# Script generated for node SQL Query
SqlQuery1096 = '''
select a.* from step_trainer as a 
inner join customer_curated as b 
on LOWER(a.serialnumber) = LOWER(b.serialnumber)
'''
SQLQuery_node1770819953313 = sparkSqlQuery(glueContext, query = SqlQuery1096, mapping = {"step_trainer":step_trainer_landing_node1770819907299, "customer_curated":customer_curated_node1770818394513}, transformation_ctx = "SQLQuery_node1770819953313")

# Script generated for node step_trainer_trusted
EvaluateDataQuality().process_rows(frame=SQLQuery_node1770819953313, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1770819883756", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
step_trainer_trusted_node1770820160683 = glueContext.getSink(path="s3://stedi-lake-house-han/trusted/step-trainer/", connection_type="s3", updateBehavior="LOG", partitionKeys=[], compression="gzip", enableUpdateCatalog=True, transformation_ctx="step_trainer_trusted_node1770820160683")
step_trainer_trusted_node1770820160683.setCatalogInfo(catalogDatabase="stedi-db",catalogTableName="step_trainer_trusted")
step_trainer_trusted_node1770820160683.setFormat("json")
step_trainer_trusted_node1770820160683.writeFrame(SQLQuery_node1770819953313)
job.commit()