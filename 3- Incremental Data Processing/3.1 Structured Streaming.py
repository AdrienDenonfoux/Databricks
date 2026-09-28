# Databricks notebook source
# MAGIC %md
# MAGIC ## Reading Stream

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE motocycles
# MAGIC AS SELECT *
# MAGIC FROM read_files(
# MAGIC     '/Volumes/demoworkspace/default/motostore_dataset/motocycle-json',
# MAGIC     format => 'json',
# MAGIC     multiLine => true
# MAGIC )

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM motocycles

# COMMAND ----------

# DBTITLE 1,Cellule 2
(spark.readStream
    .table("motocycles")
    .createOrReplaceTempView("motocycles_streaming_tmp_vw")
)

# COMMAND ----------

# DBTITLE 1,Cellule 3
# MAGIC %sql
# MAGIC SELECT * FROM motocycles_streaming_tmp_vw

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT brand, count(motocycle_id) AS total_motocycles
# MAGIC FROM motocycles_streaming_tmp_vw
# MAGIC GROUP BY brand

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TEMP VIEW brand_counts_tmp_vw AS (
# MAGIC   SELECT brand, count(motocycle_id) AS total_motocycles
# MAGIC   FROM motocycles_streaming_tmp_vw
# MAGIC   GROUP BY brand
# MAGIC );

# COMMAND ----------

# MAGIC %md
# MAGIC ## Streaming in Batch Mode

# COMMAND ----------

# MAGIC %md
# MAGIC On overide la table avec le mode complete

# COMMAND ----------

# DBTITLE 1,Cellule 5
(spark.table("brand_counts_tmp_vw")                               
      .writeStream  
      .trigger(availableNow=True)
      .outputMode("complete")
      .option("checkpointLocation", "/Volumes/demoworkspace/default/motostore_dataset/motocycle_counts_checkpoint")
      .table("motocycle_counts")
)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM motocycle_counts;
# MAGIC     

# COMMAND ----------

# MAGIC %sql
# MAGIC DROP TABLE IF EXISTS motocycle_counts;

# COMMAND ----------

# MAGIC %md
# MAGIC ## Auto Loader

# COMMAND ----------

# DBTITLE 1,Cellule 14
(spark.readStream
        .format("cloudFiles")
        .option("cloudFiles.format", "json")
        .option("cloudFiles.schemaLocation", "/Volumes/demoworkspace/default/motostore_dataset/orders_schema")
        .option("multiLine", "true")
        .load("/Volumes/demoworkspace/default/motostore_dataset/order-raw")
      .writeStream
        .option("checkpointLocation", "/Volumes/demoworkspace/default/motostore_dataset/orders_checkpoint")
        .table("orders_updates")
)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM orders_updates

# COMMAND ----------

# MAGIC %md
# MAGIC ## Loading new file

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM orders_updates

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE HISTORY orders_updates

# COMMAND ----------

# MAGIC %sql
# MAGIC DROP TABLE orders_updates

# COMMAND ----------

dbutils.fs.rm("/Volumes/demoworkspace/default/motostore_dataset/orders_checkpoint", True)