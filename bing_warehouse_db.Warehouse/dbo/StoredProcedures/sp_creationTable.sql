CREATE PROC [dbo].[sp_creationTable]

AS
BEGIN

    DROP TABLE IF EXISTS [dbo].[provider_agg];
    CREATE TABLE [dbo].[provider_agg]
     (

        provider varchar(60),
        sentiment varchar(10),
        nombre integer
    )

    INSERT INTO [dbo].[provider_agg]
    SELECT
        provider,
        sentiment,
        count(1) as nombre
    FROM bing_lake_db.Tables.tbl_sentiment_analysis
    GROUP BY provider, sentiment
    ORDER BY nombre
END