
SELECT d.Year, b.Title, SUM(f.Price) as TotalRevenue
FROM Fact_Sales f
JOIN Dim_Books b ON f.BookKey = b.BookKey
JOIN Dim_Date d ON f.OrderDateKey = d.DateKey
GROUP BY d.Year, b.Title
ORDER BY TotalRevenue DESC;