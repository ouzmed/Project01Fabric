CREATE PROC [dbo].[sp_creationTable]
AS
BEGIN

    DROP TABLE IF EXISTS bing_warehouse_db.dbo.provider_agg
    CREATE TABLE bing_warehouse_db.dbo.provider_agg
      (
        provider VARCHAR(255),
        sentiment VARCHAR(255),
        total INT
      );
    
    INSERT INTO bing_warehouse_db.dbo.provider_agg
    SELECT
        provider,
        sentiment,
        count(1) as total
    FROM bing_lake_db.dbo.tbl_sentiment_analysis
    GROUP BY provider, sentiment
END