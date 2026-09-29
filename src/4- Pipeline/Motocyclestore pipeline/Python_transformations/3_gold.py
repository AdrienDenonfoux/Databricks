# Databricks notebook source
from pyspark import pipelines as dp
from pyspark.sql import functions as F

@dp.materialized_view
def fr_daily_customer_motocycles():
    return (  spark.read.table("orders_cleaned")
                        .filter(F.col("country") == "France")
                        .groupBy(
                            "customer_id",
                            "f_name",
                            "l_name",
                            F.date_trunc("DD", F.col("order_timestamp")).alias("order_date")
                        )
                       .agg(
                            F.sum("quantity").alias("motocycle_counts")
                        )
            )