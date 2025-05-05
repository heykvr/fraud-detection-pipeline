from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("KafkaToPostgres") \
    .getOrCreate()

# Read from Kafka
df = spark.read \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "fraud-events") \
    .load()

# Transform Kafka value (binary) to string
df_parsed = df.selectExpr("CAST(value AS STRING)")

# Save to PostgreSQL
df_parsed.write \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://postgres:5432/dbs") \
    .option("dbtable", "fraud_data") \
    .option("user", "postgres") \
    .option("password", "postgres") \
    .mode("append") \
    .save()
