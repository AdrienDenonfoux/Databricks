# Databricks notebook source
data_source = "/Volumes/demoworkspace/data_ingestion"
data_destination = "/Volumes/demoworkspace/default/motostore_dataset"

# COMMAND ----------

def get_index(dir):
    files = dbutils.fs.ls(dir)
    index = 0
    if files:
        file = max(files).name
        index = int((file.rsplit('.', maxsplit=1)[0]).rsplit('_', maxsplit=1)[1])
    return index+1

# COMMAND ----------

def load_json_file(current_index):
    latest_file = f"orders_{str(current_index).zfill(2)}.json"
    print(f"Loading {latest_file} orders file to the motocyclestore dataset")
    dbutils.fs.cp(f"{streaming_dir}/{latest_file}", f"{raw_dir}/{latest_file}")

# COMMAND ----------

streaming_dir = f"{data_source}/new_order"
raw_dir = f"{data_destination}/order-raw"

def load_new_data(all=False):
    index = get_index(raw_dir)
    if index >= 10:
        print("No more data to load\n")

    elif all == True:
        while index <= 10:
            load_json_file(index)
            index += 1
    else:
        load_json_file(index)
        index += 1