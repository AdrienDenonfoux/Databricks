# Databricks notebook source
#customers_df = spark.read.table("customer")
customers_df = spark.table("customer")
display(customers_df.select("customer_id","email"))

# COMMAND ----------

from pyspark.sql.functions import col
display(customers_df.select(col("customer_id"),col("email").alias("email_address"), col("updated").cast("timestamp"))) 

# COMMAND ----------

display(customers_df.drop("profile", "updated"))

# COMMAND ----------

from pyspark.sql.functions import col, split

new_customers_df = customers_df.withColumn("customer_domain", split(col("email"), "@").getItem(1)) \
    .withColumnRenamed("email", "customer_email") \
    .drop("profile", "updated")
 
display(new_customers_df)

# new_customers_df = (
#                     customers_df.withColumn("customer_domain", F.split(F.col("email"), "@").getItem(1))
#                                 .withColumnRenamed("email", "customer_email")
#                                 .drop("profile", "updated")
#                     )

# COMMAND ----------

orders_df = spark.table("orders")

display(orders_df.describe())
#display(orders_df.summary())

# COMMAND ----------

# MAGIC %md
# MAGIC ## Data Deduplication

# COMMAND ----------

orders_df = spark.table("orders")
display(orders_df)

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO orders
# MAGIC VALUES ('C00025', NULL, 'O00001', 7, NULL, 100.0, null)

# COMMAND ----------

#deduped_df = orders_df.distinct()
#deduped_df = orders_df.dropDuplicates()

deduped_df = orders_df.dropDuplicates(["order_id","customer_id"])
display(deduped_df)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Null Handling

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO customer(customer_id)
# MAGIC VALUES ("C00031");
# MAGIC
# MAGIC INSERT INTO customer(customer_id)
# MAGIC VALUES ("C00032");

# COMMAND ----------

customers_df = spark.table("customer")
display(customers_df)

# COMMAND ----------

#clean_df = customers_df.fillna({"email": "unknown@example.com"})
clean_df = customers_df.na.fill({"email": "unknown@example.com"})
display(clean_df)

# COMMAND ----------

#clean_df = customers_df.dropna()
clean_df = customers_df.na.drop(subset=["first_name"])
display(clean_df)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Join

# COMMAND ----------

joined_df = customers_df.join(orders_df, "customer_id", "left")
display(joined_df)

# COMMAND ----------

anti_joined_df = customers_df.join(orders_df, "customer_id", "left_anti")
display(anti_joined_df)

# COMMAND ----------

display(orders_df.where("customer_id = 'C00005'"))

# COMMAND ----------

motocycles_df = spark.table("motocycles")
orders_df = spark.table("orders")

# COMMAND ----------

from pyspark.sql.functions import explode, broadcast

exploded_orders_df = (orders_df.withColumn("motocycle", explode("motocycles"))
                                .select("*", "motocycle.motocycle_id", "motocycle.subtotal")
                                .drop("motocycles", "motocycle")
                     )

orders_details_df = exploded_orders_df.join(broadcast(motocycles_df), "motocycle_id", "inner")
display(orders_details_df)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 
# MAGIC Querying Data

# COMMAND ----------

# DBTITLE 1,Cellule 22
customers_details_df = spark.sql("""SELECT customer_id, email, updated,
                                        profile.first_name,
                                        profile.last_name,
                                        profile.gender,
                                        profile.adresse.street,
                                        profile.adresse.city,
                                        profile.adresse.country
                                    FROM customer
                                """)

display(customers_details_df)

# COMMAND ----------

customers_details_df.write.mode("overwrite").saveAsTable("customers_details")

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM customers_details