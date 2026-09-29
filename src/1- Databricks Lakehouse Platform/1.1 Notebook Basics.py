# Databricks notebook source
# MAGIC %md
# MAGIC # Simple notebook
# MAGIC
# MAGIC - Test basics scripts
# MAGIC - Run notebook
# MAGIC - Magic command %fs or dbutils
# MAGIC
# MAGIC
# MAGIC ![Associate-badge](https://www.databricks.com/wp-content/uploads/2022/04/associate-badge-eng.svg)

# COMMAND ----------

print("Hello World!")

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT "Hello World form SQL!"

# COMMAND ----------

# MAGIC %run ./Setup

# COMMAND ----------

print(f"Je m'appelle : {user_name}")

# COMMAND ----------

# MAGIC %fs ls '/databricks-datasets'

# COMMAND ----------

files = dbutils.fs.ls('/databricks-datasets')
display(files)