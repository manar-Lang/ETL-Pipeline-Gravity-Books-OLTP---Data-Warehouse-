# %%
import pyodbc
import pandas as pd


conn_str = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=.;DATABASE=Gravity_Books;Trusted_Connection=yes;"
dwh_str = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=.;DATABASE=GravityBooks_DWH;Trusted_Connection=yes;"

src_conn = pyodbc.connect(conn_str)
dest_conn = pyodbc.connect(dwh_str)

# 1. Extract & Transform
query = """
SELECT b.book_id, b.title, l.language_name, p.publisher_name
FROM book b
JOIN book_language l ON b.language_id = l.language_id
JOIN publisher p ON b.publisher_id = p.publisher_id
"""
df_books = pd.read_sql(query, src_conn)

# 2. Load
cursor = dest_conn.cursor()
for index, row in df_books.iterrows():
    cursor.execute("INSERT INTO Dim_Books (BookID, Title, Language_Name, Publisher_Name) VALUES (?,?,?,?)",
                   row.book_id, row.title, row.language_name, row.publisher_name)
dest_conn.commit()
print("Dim_Books Loaded!")

# %%
# Extract Orders
sales_query = """
SELECT b.book_id, o.customer_id, ol.price, o.order_date
FROM cust_order o
JOIN order_line ol ON o.order_id = ol.order_id
JOIN book b ON ol.book_id = b.book_id
"""
df_sales = pd.read_sql(sales_query, src_conn)



# %%
import pyodbc

conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                      'SERVER=.;' 
                      'DATABASE=GravityBooks_DWH;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()

sql_command = """
INSERT INTO Fact_Sales (BookKey, CustomerKey, OrderDateKey, Price)
SELECT 
    b.BookKey, 
    c.CustomerKey, 
    CAST(FORMAT(src_o.order_date, 'yyyyMMdd') AS INT), 
    src_ol.price
FROM Gravity_Books.dbo.cust_order src_o
JOIN Gravity_Books.dbo.order_line src_ol ON src_o.order_id = src_ol.order_id
INNER JOIN Dim_Books b ON src_ol.book_id = b.BookID
INNER JOIN Dim_Customers c ON src_o.customer_id = c.CustomerID;
"""

import pandas as pd
import pyodbc


src_conn = pyodbc.connect('DRIVER={SQL Server};SERVER=.;DATABASE=Gravity_Books;Trusted_Connection=yes;')

print("جاري سحب البيانات من المصدر...")
df_books = pd.read_sql("SELECT * FROM book", src_conn)
df_customers = pd.read_sql("SELECT * FROM customer", src_conn)
df_orders = pd.read_sql("SELECT * FROM cust_order", src_conn)
df_order_lines = pd.read_sql("SELECT * FROM order_line", src_conn)


df_fact = pd.merge(df_orders, df_order_lines, on='order_id')


df_fact.to_csv(r'C:\Task etl eng abdelrahman\Fact_Sales_Output.csv', index=False, encoding='utf-8-sig')
df_customers.to_csv(r'C:\Task etl eng abdelrahman\Customers_Output.csv', index=False, encoding='utf-8-sig')

print(f"تم بنجاح! تم حفظ {len(df_fact)} سجل مبيعات في الملف.")

src_conn.close()

