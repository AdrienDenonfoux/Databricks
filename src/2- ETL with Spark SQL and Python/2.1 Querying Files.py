# Databricks notebook source
dataset_moto = "/Volumes/demoworkspace/default/motostore_dataset"

# COMMAND ----------

files = dbutils.fs.ls(f"{dataset_moto}/customer-json")
display(files)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Lecture de fichiers

# COMMAND ----------

# DBTITLE 1,Cellule 3
# MAGIC %sql
# MAGIC SELECT *, _metadata.file_path
# MAGIC FROM read_files(
# MAGIC   '/Volumes/demoworkspace/default/motostore_dataset/customer-json',
# MAGIC   format => 'json',
# MAGIC   multiLine => true
# MAGIC )

# COMMAND ----------

# DBTITLE 1,Cellule 4
# MAGIC %sql
# MAGIC DROP TABLE customer_csv;
# MAGIC CREATE OR REPLACE TABLE customer_csv AS
# MAGIC SELECT * FROM read_files(
# MAGIC     '/Volumes/demoworkspace/default/motostore_dataset/customer-csv/customers_4.csv',
# MAGIC     format => 'csv',
# MAGIC     header => true,
# MAGIC     delimiter => ',',
# MAGIC     schema => 'customer_id STRING, email STRING, first_name STRING, last_name STRING, gender STRING, street STRING, city STRING, country STRING, updated STRING, _rescued_data STRING'
# MAGIC )

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM customer_csv

# COMMAND ----------

# DBTITLE 1,Cellule 7
(spark.read
  .table("customer_csv")
  .write
  .format("csv")
  .option('header', 'true')
  .option('delimiter', ',')
  .mode("overwrite")
  .save(f"{dataset_moto}/customer-csv/result")
)

# COMMAND ----------

files = dbutils.fs.ls(f"{dataset_moto}/customer-csv/result")
display(files)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM customer_csv

# COMMAND ----------

# MAGIC %sql
# MAGIC REFRESH TABLE customer_csv

# COMMAND ----------

# DBTITLE 1,Cellule 11
# MAGIC %sql
# MAGIC INSERT OVERWRITE customer_csv
# MAGIC SELECT * FROM read_files(
# MAGIC   '/Volumes/demoworkspace/default/motostore_dataset/customer-csv',
# MAGIC   format => 'csv',
# MAGIC   header => true,
# MAGIC   delimiter => ',',
# MAGIC   schema => 'customer_id STRING, email STRING, first_name STRING, last_name STRING, gender STRING, street STRING, city STRING, country STRING, updated STRING, _rescued_data STRING'
# MAGIC )

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM customer_csv

# COMMAND ----------

# MAGIC %md
# MAGIC ## Merging Data

# COMMAND ----------

# MAGIC %md
# MAGIC C00031,louis651@protonmail.com,Louis,Petrov,Female,58 Rue Victor Hugo,New York,United States,2024-08-09T00:00:00Z

# COMMAND ----------

# MAGIC %sql
# MAGIC UPDATE customer_csv
# MAGIC SET email = NULL
# MAGIC WHERE customer_id = 'C00031'

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM customer_csv

# COMMAND ----------

# DBTITLE 1,Cellule 13
# MAGIC %sql
# MAGIC CREATE OR REPLACE TEMP VIEW customers_updates AS 
# MAGIC SELECT * FROM read_files(
# MAGIC   '/Volumes/demoworkspace/default/motostore_dataset/customer-new/customers_5.csv',
# MAGIC   format => 'csv',
# MAGIC   header => true,
# MAGIC   delimiter => ','
# MAGIC );

# COMMAND ----------

# MAGIC %sql
# MAGIC MERGE INTO customer_csv c
# MAGIC USING customers_updates u
# MAGIC ON c.customer_id = u.customer_id
# MAGIC WHEN MATCHED AND c.email IS NULL AND u.email IS NOT NULL THEN
# MAGIC   UPDATE SET email = u.email, updated = u.updated
# MAGIC WHEN NOT MATCHED THEN INSERT *

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE motocycles (
# MAGIC     motocycle_id STRING,
# MAGIC     name STRING,
# MAGIC     category STRING,
# MAGIC     engine_displacement_cc INT,
# MAGIC     horsepower INT,
# MAGIC     brand STRING,
# MAGIC     price NUMERIC(10,2)
# MAGIC );

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TEMP VIEW motocycle_updates
# MAGIC AS SELECT * FROM read_files(
# MAGIC   '/Volumes/demoworkspace/default/motostore_dataset/motocycle-new/motocycles_new.json',
# MAGIC   format => 'json',
# MAGIC   multiLine => true
# MAGIC );
# MAGIC
# MAGIC SELECT * FROM motocycle_updates

# COMMAND ----------

# MAGIC %sql
# MAGIC MERGE INTO motocycles m
# MAGIC USING motocycle_updates u
# MAGIC ON m.motocycle_id = u.motocycle_id AND m.name = u.name
# MAGIC WHEN NOT MATCHED AND u.category = 'Sport' THEN 
# MAGIC   INSERT *

# COMMAND ----------

# MAGIC %md
# MAGIC ## Parsing JSON Data

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE customers
# MAGIC AS SELECT * FROM read_files(
# MAGIC   '/Volumes/demoworkspace/default/motostore_dataset/customer-json',
# MAGIC   format => 'json',
# MAGIC   multiLine => true
# MAGIC );

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT customer_id, profile.first_name, profile.adresse.country 
# MAGIC FROM customers

# COMMAND ----------

# MAGIC %md
# MAGIC ## Explode Function

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE orders
# MAGIC AS SELECT * FROM read_files(
# MAGIC   '/Volumes/demoworkspace/default/motostore_dataset/order-json',
# MAGIC   format => 'json',
# MAGIC   multiLine => true
# MAGIC );

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT order_id, customer_id, explode(motocycles)
# MAGIC FROM orders

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT customer_id,
# MAGIC   collect_set(order_id) AS orders_set,
# MAGIC   collect_set(motocycles.motocycle_id) AS motcycles_set
# MAGIC FROM orders
# MAGIC GROUP BY customer_id

# COMMAND ----------

# DBTITLE 1,Cellule 28
# MAGIC %sql
# MAGIC SELECT customer_id,
# MAGIC   collect_set(motocycles.motocycle_id) As before_flatten,
# MAGIC   array_distinct(flatten(collect_set(motocycles.motocycle_id))) AS after_flatten
# MAGIC FROM orders
# MAGIC GROUP BY customer_id

# COMMAND ----------

# MAGIC %md
# MAGIC ## Join operation

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *, explode(motocycles) AS motocycle 
# MAGIC   FROM orders

# COMMAND ----------

# DBTITLE 1,Cellule 30
# MAGIC %sql
# MAGIC CREATE OR REPLACE VIEW orders_enriched AS
# MAGIC SELECT *
# MAGIC FROM (
# MAGIC   SELECT *, explode(motocycles) AS motocycle 
# MAGIC   FROM orders) o
# MAGIC INNER JOIN motocycles m
# MAGIC ON o.motocycle.motocycle_id = m.motocycle_id;
# MAGIC
# MAGIC SELECT * FROM orders_enriched

# COMMAND ----------

# MAGIC %md
# MAGIC ## Filtering Arrays

# COMMAND ----------

# MAGIC %md
# MAGIC ### Liste les order avec plus ou deux moto acheté

# COMMAND ----------

# DBTITLE 1,Cellule 34
# MAGIC %sql
# MAGIC SELECT
# MAGIC   order_id,
# MAGIC   motocycles,
# MAGIC   FILTER (motocycles, i -> i.quantity >= 2) AS multiple_copies
# MAGIC FROM orders

# COMMAND ----------

# MAGIC %md
# MAGIC # Liste les order avec plus ou deux moto acheté mais sans afficher les customers qui n'ont rien acheté.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT order_id, multiple_copies
# MAGIC FROM (
# MAGIC   SELECT
# MAGIC     order_id,
# MAGIC     FILTER (motocycles, i -> i.quantity >= 2) AS multiple_copies
# MAGIC   FROM orders)
# MAGIC WHERE size(multiple_copies) > 0;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM orders

# COMMAND ----------

# MAGIC %md
# MAGIC ## Transforming Arrays

# COMMAND ----------

# DBTITLE 1,Cellule 38
# MAGIC %sql
# MAGIC SELECT
# MAGIC   order_id,
# MAGIC   motocycles,
# MAGIC   TRANSFORM (
# MAGIC     motocycles,
# MAGIC     b -> CAST(b.subtotal * 0.8 AS INT)
# MAGIC   ) AS subtotal_after_discount
# MAGIC FROM orders;

# COMMAND ----------

# MAGIC %md
# MAGIC ## User Defined Functions (UDF)

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE FUNCTION get_url(email STRING)
# MAGIC RETURNS STRING
# MAGIC
# MAGIC RETURN concat("https://www.", split(email, "@")[1])

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT email, get_url(email) domain
# MAGIC FROM customer_csv

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE FUNCTION EXTENDED get_url

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE FUNCTION site_type(email STRING)
# MAGIC RETURNS STRING
# MAGIC RETURN CASE 
# MAGIC           WHEN email like "%.com" THEN "Commercial business"
# MAGIC           WHEN email like "%.org" THEN "Non-profits organization"
# MAGIC           WHEN email like "%.edu" THEN "Educational institution"
# MAGIC           ELSE concat("Unknow extenstion for domain: ", split(email, "@")[1])
# MAGIC        END;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT email, site_type(email) as domain_category
# MAGIC FROM customer_csv

# COMMAND ----------

# MAGIC %sql
# MAGIC DROP FUNCTION get_url;
# MAGIC DROP FUNCTION site_type;