SELECT TOP 10 
    f.Price, 
    b.Title AS Book_Name, 
    c.Full_Name AS Customer, 
    d.FullDate AS Sale_Date
FROM Fact_Sales f
JOIN Dim_Books b ON f.BookKey = b.BookKey
JOIN Dim_Customers c ON f.CustomerKey = c.CustomerKey
JOIN Dim_Date d ON f.OrderDateKey = d.DateKey;