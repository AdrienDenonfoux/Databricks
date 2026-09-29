# Databricks notebook source
# MAGIC %sql
# MAGIC SELECT * FROM demoworkspace.motocycle_bundle.sp_daily_customer_motocycles

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM demoworkspace.motocycle_bundle.fr_daily_customer_motocycles

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT SUM(total) AS revenue FROM demoworkspace.motocycle_bundle.orders_raw

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) AS nb_orders FROM demoworkspace.motocycle_bundle.orders_raw

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT AVG(total) AS avg_basket FROM demoworkspace.motocycle_bundle.orders_raw

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(DISTINCT customer_id) AS active_customers FROM demoworkspace.motocycle_bundle.orders_raw

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   m.motocycle_id,
# MAGIC   m.quantity,
# MAGIC   m.subtotal,
# MAGIC   o.order_id,
# MAGIC   o.customer_id,
# MAGIC   o.timestamp
# MAGIC FROM demoworkspace.motocycle_bundle.orders_raw o
# MAGIC LATERAL VIEW explode(o.motocycles) exploded AS m