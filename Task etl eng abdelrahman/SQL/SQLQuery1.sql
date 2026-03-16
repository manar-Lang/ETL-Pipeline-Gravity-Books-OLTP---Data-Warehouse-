SELECT 'Date Dimension' AS TableName, COUNT(*) AS Total FROM Dim_Date
UNION ALL
SELECT 'Customers Dimension', COUNT(*) FROM Dim_Customers
UNION ALL
SELECT 'Sales Fact', COUNT(*) FROM Fact_Sales;