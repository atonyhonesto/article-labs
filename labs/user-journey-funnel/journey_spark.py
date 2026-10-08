"""Reference: the same sessionisation in PySpark (not run in CI; shown for the article)."""
SPARK_EQUIVALENT = '''
from pyspark.sql import functions as F, Window

w = Window.partitionBy("user_id").orderBy("ts")
events = (events
    .withColumn("gap_s", F.col("ts").cast("long") - F.lag(F.col("ts").cast("long")).over(w))
    .withColumn("new_session", (F.col("gap_s").isNull() | (F.col("gap_s") > 1800)).cast("int"))
    .withColumn("session_id", F.concat_ws("-", "user_id", F.sum("new_session").over(w))))
'''
