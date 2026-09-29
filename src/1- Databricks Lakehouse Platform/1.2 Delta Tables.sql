-- Databricks notebook source
USE CATALOG demoworkspace

-- COMMAND ----------

CREATE OR REPLACE TABLE employees
  (id INT, name STRING, salary DOUBLE);

-- COMMAND ----------

INSERT INTO employees
VALUES 
  (1, "Adam", 3500.0),
  (2, "Sarah", 4020.5);

INSERT INTO employees
VALUES
  (3, "John", 2999.3),
  (4, "Thomas", 4000.3);

INSERT INTO employees
VALUES
  (5, "Anna", 2500.0);

INSERT INTO employees
VALUES
  (6, "Kim", 6200.3)

-- COMMAND ----------

SELECT * FROM employees

-- COMMAND ----------

DESCRIBE DETAIL employees

-- COMMAND ----------

DESCRIBE HISTORY employees

-- COMMAND ----------

UPDATE employees 
SET salary = salary + 100
WHERE name LIKE "A%"

-- COMMAND ----------

DESCRIBE HISTORY employees

-- COMMAND ----------

SELECT * FROM employees VERSION AS OF 4
-- SELECT * FROM employees@v4

-- COMMAND ----------

RESTORE TABLE employees TO VERSION AS OF 5

-- COMMAND ----------

DESCRIBE HISTORY employees

-- COMMAND ----------

-- MAGIC %md
-- MAGIC # OPTIMIZE Command

-- COMMAND ----------

DESCRIBE DETAIL employees

-- COMMAND ----------

OPTIMIZE employees 
ZORDER BY id

-- COMMAND ----------

DESCRIBE DETAIL employees

-- COMMAND ----------

DESCRIBE HISTORY employees

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Commande utile

-- COMMAND ----------

-- MAGIC %md
-- MAGIC _delta_log est un repertoire stockant les fichiers de gestions de la delta table

-- COMMAND ----------

-- MAGIC %fs ls 'dbfs:/user/hive/warehouse/employees/_delta_log'

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## VACUUM Command
-- MAGIC
-- MAGIC Permet de nettoyer les fichiers de gestion d'une delta table (plus de 7 jours après création)

-- COMMAND ----------

VACUUM employees RETAIN 168 HOURS

-- COMMAND ----------

-- MAGIC %md
-- MAGIC # MANAGED OR EXTERNAL TABLE

-- COMMAND ----------

CREATE TABLE managed_default
  (width INT, length INT, height INT);

INSERT INTO managed_default
VALUES (3 INT, 2 INT, 1 INT)

-- COMMAND ----------

DESCRIBE EXTENDED managed_default

-- COMMAND ----------

-- DBTITLE 1,Cellule 25
CREATE OR REPLACE TABLE external_default
  (width INT, length INT, height INT)
LOCATION 'abfss://unity-catalog-storage@dbstoragetvt2q5j2w2v26.dfs.core.windows.net/7405618176164444/external_default';

INSERT INTO external_default
VALUES (3 INT, 2 INT, 1 INT)

-- COMMAND ----------

DESCRIBE EXTENDED external_default

-- COMMAND ----------

CREATE SCHEMA new_default

-- COMMAND ----------

DESCRIBE DATABASE EXTENDED new_default

-- COMMAND ----------

USE new_default;

CREATE TABLE managed_new_default
  (width INT, length INT, height INT);
  
INSERT INTO managed_new_default
VALUES (3 INT, 2 INT, 1 INT);

-----------------------------------

CREATE TABLE external_new_default
  (width INT, length INT, height INT)
LOCATION 'abfss://unity-catalog-storage@dbstoragetvt2q5j2w2v26.dfs.core.windows.net/7405618176164444/external_new_default';
  
INSERT INTO external_new_default
VALUES (3 INT, 2 INT, 1 INT);

-- COMMAND ----------

DESCRIBE EXTENDED managed_new_default

-- COMMAND ----------

DESCRIBE EXTENDED external_new_default

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## # Creating Schemas in Custom Location

-- COMMAND ----------

CREATE SCHEMA custom
LOCATION 'dbfs:/Shared/schemas/custom.db'