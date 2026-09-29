-- Databricks notebook source
CREATE OR REFRESH MATERIALIZED VIEW sp_daily_customer_motocycles
COMMENT "Daily number of motocycles per customer in Spain"
AS
  SELECT customer_id, f_name, l_name, date_trunc("DD", order_timestamp) order_date, sum(quantity) motocycles_counts
  FROM orders_cleaned
  WHERE country = "Spain"
  GROUP BY customer_id, f_name, l_name, date_trunc("DD", order_timestamp)

-- COMMAND ----------

CREATE OR REFRESH MATERIALIZED VIEW fr_daily_customer_motocycles
COMMENT "Daily number of motocycles per customer in France"
AS
  SELECT customer_id, f_name, l_name, date_trunc("DD", order_timestamp) order_date, sum(quantity) motocycles_counts
  FROM orders_cleaned
  WHERE country = "France"
  GROUP BY customer_id, f_name, l_name, date_trunc("DD", order_timestamp)