-- Databricks notebook source
CREATE OR REFRESH STREAMING TABLE orders_cleaned (
  CONSTRAINT positive_quantity  EXPECT (quantity > 0) ON VIOLATION DROP ROW,
  CONSTRAINT valid_customer EXPECT (f_name IS NOT NULL AND l_name IS NOT NULL) ON VIOLATION FAIL UPDATE,
  CONSTRAINT recent_order EXPECT (order_timestamp >= "2022-07-15")
)
COMMENT "The cleaned motocycles orders with valid order_id"
AS
  SELECT order_id, quantity, o.customer_id, c.profile.first_name as f_name, c.profile.last_name as l_name,
         cast(o.timestamp AS timestamp) as order_timestamp, o.motocycles,
         c.profile.adresse.country as country
  FROM STREAM orders_raw o
  LEFT JOIN customers c
  ON o.customer_id = c.customer_id;