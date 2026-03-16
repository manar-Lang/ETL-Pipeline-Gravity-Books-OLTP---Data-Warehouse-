SELECT TOP 5 c.Full_Name, SUM(f.Price) AS Total_Spent
FROM Fact_Sales f
JOIN Dim_Customers c ON f.CustomerKey = c.CustomerKey
GROUP BY c.Full_Name
ORDER BY Total_Spent DESC;