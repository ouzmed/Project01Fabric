# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "6e63736d-c7dc-465f-a1ab-2e53bfcb104d",
# META       "default_lakehouse_name": "bing_lake_db",
# META       "default_lakehouse_workspace_id": "1237831a-c12b-499a-9dcd-7f59f765fda8"
# META     }
# META   }
# META }

# CELL ********************

# Welcome to your new notebook
# Type here in the cell editor to add code!


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df = spark.read.option("multiline", "true").json("Files/bing-latest-news.json")
# df now is a Spark DataFrame containing JSON data from "Files/bing-latest-news.json".
display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df = df.select("value")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql.functions import explode
df_explode = df.select(explode(df["value"]).alias("json_object"))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

display(df_explode)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# Converting the exploded json dataframe to a single json string list

# CELL ********************

json_list = df_explode.toJSON().collect()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# testing the json string list

# CELL ********************

print(json_list[1])

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

import json

news_json = json.loads(json_list[1])
print(news_json)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

print(news_json['json_object']['name'])
print(news_json['json_object']['description'])
print(news_json['json_object']['url'])
#print(news_json['json_object']['provider']['image']['thumbnail']['contentUrl'])
print(news_json['json_object']['provider'][0]['name'])
print(news_json['json_object']['datePublished'])

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

description =[]
title =[]
image =[]
url =[]
provider =[]
datePublished =[]

#process each JSON object in the list

for js_str in json_list:
    try:
        #parse the json into a dictionary
        article = json.loads(js_str)

        #extract information from the dictionary
        description.append(article['json_object']['description'])
        title.append(article['json_object']['name'])
        image.append(article['json_object']['provider'][0]['image']['thumbnail']['contentUrl'])
        url.append(article['json_object']['url'])
        provider.append(article['json_object']['provider'][0]['name'])
        datePublished.append(article['json_object']['datePublished'])
    except Exception as e:
        print(f"Error processing JSON object:{e}")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql.types import StructField, StructType, StringType

#combine the lists:
data = list(zip(title, description, image, url, provider, datePublished))

#define schema:
schema = StructType([
    StructField('title', StringType(), True),
    StructField('description', StringType(), True),
    StructField('image', StringType(), True),
    StructField('url', StringType(), True),
    StructField('provider', StringType(), True),
    StructField('datePublished', StringType(), True),
])

#create dataframe:
df_final = spark.createDataFrame(data = data, schema= schema)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

display(df_final)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql.functions import to_date, date_format

df_cleaned_final = df_final.withColumn("datePublished", date_format(to_date("datePublished"), "dd-MMM-yyyy"))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

display(df_cleaned_final)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# Read the JSON file as a Dataframe

# CELL ********************

df = spark.read.option("multiline", "true").json("Files/bing-latest-news.json")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
