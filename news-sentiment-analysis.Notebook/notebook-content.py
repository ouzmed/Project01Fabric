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

df = spark.sql("SELECT * FROM bing_lake_db.tbl_latest_news")
display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

import synapse.ml.core
from synapse.ml.services import AnalyzeText

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

#Import the model and configure the input and output columns

model = (AnalyzeText()
        .setTextCol("description")
        .setKind("SentimentAnalysis")
        .setOutputCol("response")
        .setErrorCol("error"))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

#Apply the model to our dataframe
result = model.transform(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

display(result)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

#create Sentiment Column
from pyspark.sql.functions import col

sentiment_df = result.withColumn("sentiment", col("response.documents.sentiment"))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

display(sentiment_df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## remove unwanted columns

# CELL ********************

sentiment_df_final = sentiment_df.drop("error","response")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

display(sentiment_df_final)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql.functions import col, to_date

sentiment_df_final = sentiment_df_final.withColumn("datePublished", to_date(col("datePublished"), "dd-MMM-yyyy"))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Type 1 Merge

# CELL ********************

from pyspark.sql.utils import AnalysisException

try:
    table_name = 'bing_lake_db.tbl_sentiment_analysis'
    sentiment_df_final.write.format("delta").saveAsTable(table_name)

except AnalysisException:

    print("Table Already Exists")
    
    sentiment_df_final.createOrReplaceTempView("vw_sentiment_df_final")

    spark.sql(f"""  MERGE INTO {table_name} target_table
                    USING vw_sentiment_df_final source_view

                    ON source_view.url = target_table.url

                    WHEN MATCHED AND
                    source_view.title <> target_table.title OR
                    source_view.description <> target_table.description OR
                    source_view.image <> target_table.image OR
                    source_view.provider <> target_table.provider OR
                    source_view.datePublished <> target_table.datePublished

                    THEN UPDATE SET *

                    when NOT MATCHED THEN INSERT *


            """)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
