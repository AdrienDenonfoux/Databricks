-- Databricks notebook source
CREATE OR REFRESH STREAMING TABLE orders_raw
COMMENT "The raw motocycles orders, ingested from order_raw"
AS SELECT * FROM STREAM read_files("${dataset_path}/order-raw", 
                                    format => 'json',
                                    multiLine => true);
 

CREATE OR REFRESH MATERIALIZED VIEW customers
COMMENT "The customers lookup table, ingested from customer-json"
AS SELECT * FROM read_files("${dataset_path}/customer-json", 
                                    format => 'json',
                                    multiLine => true);