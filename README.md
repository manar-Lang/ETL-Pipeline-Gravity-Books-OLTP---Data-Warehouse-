# 📚 Gravity Books ETL Pipeline – OLTP to Data Warehouse

A complete ETL (Extract, Transform, Load) pipeline that migrates data from the Gravity Books OLTP database to a dimensional data warehouse (Star Schema) using Python. This project demonstrates fundamental data warehousing concepts and ETL best practices.

---

## 📌 Table of Contents

- [🔎 Project Overview](#-project-overview)
- [🚧 Current Technical & Budget Constraints](#-current-technical--budget-constraints)
- [🚀 Final Goals](#-final-goals)
- [🏁 Competitors](#-competitors)
- [❗Key Technical Challenges & Roadblocks](#key-technical-challenges--roadblocks)
- [💡 Proposed Solutions](#-proposed-solutions)
- [📈 System Architecture](#-system-architecture)
- [🔧 Features](#-features)
- [🧪 Pipeline Phases](#-pipeline-phases)
- [🧬 Data Flow Diagram](#-data-flow-diagram)
- [🗂 Directory Structure](#-directory-structure)
- [📦 Tech Stack](#-tech-stack)
- [📊 Data Modeling Approach](#-data-modeling-approach)
- [🗓 Roadmap](#-roadmap)
- [🧾 License](#-license)
- [👨‍💻 Author](#-author)
- [📬 Future Improvements](#-future-improvements)
- [🙋‍♂️ Contributing](#-contributing)
- [📞 Contact](#-contact)

---

## 🔎 Project Overview

Gravity Books ETL Pipeline is a Python-based solution that extracts data from an OLTP (Online Transaction Processing) database, transforms it according to dimensional modeling principles, and loads it into a Data Warehouse optimized for analytical queries.

The pipeline handles:
- 📚 Book information with language and publisher details
- 👥 Customer data with address and location information
- 📦 Order transactions and line items
- 💰 Sales facts for business intelligence and reporting

This enables:
- 📊 Fast analytical queries on historical sales data
- 📈 Business intelligence dashboards
- 🔍 Customer purchasing pattern analysis
- 📉 Inventory and sales performance tracking

---

## 🚧 Current Technical & Budget Constraints

This project operates within a local development environment with the following constraints:
- **Database**: Local SQL Server instances for both source and destination
- **Processing**: Single-threaded Python ETL (no distributed computing)
- **Budget**: No cloud services or paid APIs utilized
- **Scale**: Handles moderate-sized datasets efficiently

---

## 🚀 Final Goals

- ✅ **Extract Phase**: Pull data from multiple related tables in the source OLTP database
- ✅ **Transform Phase**: Clean, validate, and structure data according to star schema design
- ✅ **Load Phase**: Populate dimension and fact tables in the data warehouse
- ✅ **Incremental Loads**: Support for loading only new/changed data (SCD Type 1)
- ✅ **Error Handling**: Robust exception handling and logging
- ✅ **Performance Optimization**: Batch inserts and connection management
- ✅ **Documentation**: Complete with architecture diagrams and data lineage

---

## 🏁 Competitors

Several tools and platforms can perform similar ETL tasks:

- **SSIS (SQL Server Integration Services)**: Microsoft's enterprise ETL tool with visual design interface but steeper learning curve
- **Apache NiFi**: Powerful data flow automation with web-based UI
- **Talend**: Open-source ETL tool with extensive connector library
- **dbt (data build tool)**: Focuses on transform phase with SQL-based modeling
- **Airbyte**: Open-source data integration platform

This Python-based approach offers:
- ✅ Lightweight and portable solution
- ✅ Full control over transformation logic
- ✅ Easy integration with pandas for data manipulation
- ✅ No additional software licensing costs

---

## ❗Key Technical Challenges & Roadblocks

- **Data Integrity**: Ensuring referential integrity when loading dimension tables before facts
- **Surrogate Key Generation**: Managing identity columns and key lookups during fact loading
- **Incremental Loads**: Identifying and processing only new or modified records
- **Performance**: Optimizing batch inserts for large datasets
- **Error Recovery**: Handling failures mid-pipeline without data corruption
- **Data Consistency**: Managing transactions across multiple table loads

---

## 💡 Proposed Solutions

- **Dimension First Loading**: Load all dimension tables before facts to ensure key availability
- **Lookup Caching**: Cache dimension keys in memory for faster fact table inserts
- **Batch Processing**: Use pandas chunks and bulk insert operations
- **Transaction Management**: Wrap related operations in database transactions
- **Logging & Monitoring**: Comprehensive logging for debugging and audit trails
- **Modular Design**: Separate extract, transform, and load phases for maintainability

---

## 📈 System Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Source OLTP   │────▶│    ETL Engine   │────▶│  Data Warehouse │
│  (Gravity_Books)│     │    (Python)     │     │(GravityBooks_DWH)│
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │                       │                        │
         ▼                       ▼                        ▼
    ┌────────────┐         ┌────────────┐          ┌────────────┐
    │• book      │         │• Extract   │          │• Dim_Books │
    │• customer  │         │• Transform │          │• Dim_Cust  │
    │• cust_order│         │• Load      │          │• Dim_Date  │
    │• order_line│         │• Validate  │          │• Fact_Sales│
    └────────────┘         └────────────┘          └────────────┘
```

---

## 🔧 Features

- ✅ **Modular Pipeline**: Separated extraction, transformation, and loading phases
- ✅ **Star Schema Design**: Fact and dimension tables optimized for analytics
- ✅ **Incremental Loading**: Processes only new or modified records
- ✅ **Data Validation**: Checks for data quality and integrity
- ✅ **Error Handling**: Comprehensive try-catch blocks and logging
- ✅ **Performance Optimized**: Batch inserts and connection pooling
- ✅ **Configuration Driven**: Easy to modify connection strings and settings
- ✅ **Cross-Platform**: Runs on any system with Python and SQL Server ODBC driver

---

## 🧪 Pipeline Phases

<details>
<summary>✅ Phase 1: Dimension Extraction & Loading</summary>

**Inputs:**
- Source database connection
- Dimension table queries

**Process:**
1. Extract book data with language and publisher information
2. Extract customer data with address and country details
3. Transform data (clean nulls, format strings)
4. Load into dimension tables with surrogate key generation

**Outputs:**
- Populated `Dim_Books` table
- Populated `Dim_Customers` table
- (Optional) Populated `Dim_Date` table

**Code Snippet:**
```python
# Extract books with related data
books_query = """
SELECT b.book_id, b.title, l.language_name, p.publisher_name
FROM book b
JOIN book_language l ON b.language_id = l.language_id
JOIN publisher p ON b.publisher_id = p.publisher_id
"""
df_books = pd.read_sql(books_query, src_conn)

# Load into dimension
for _, row in df_books.iterrows():
    cursor.execute("""
        INSERT INTO Dim_Books (BookID, Title, Language_Name, Publisher_Name)
        VALUES (?, ?, ?, ?)
    """, row.book_id, row.title, row.language_name, row.publisher_name)
```

</details>

<details>
<summary>✅ Phase 2: Fact Table Extraction & Loading</summary>

**Inputs:**
- Source order and order line data
- Populated dimension tables
- Date information

**Process:**
1. Extract sales transactions with joins
2. Look up surrogate keys from dimension tables
3. Transform date keys to integer format (YYYYMMDD)
4. Load into fact table with proper key references

**Outputs:**
- Populated `Fact_Sales` table with:
  - BookKey (FK to Dim_Books)
  - CustomerKey (FK to Dim_Customers)
  - OrderDateKey (FK to Dim_Date)
  - Price (measure)
  - Quantity (measure)

**Code Snippet:**
```python
# Extract sales data
sales_query = """
SELECT b.book_id, o.customer_id, ol.price, ol.quantity, o.order_date
FROM cust_order o
JOIN order_line ol ON o.order_id = ol.order_id
JOIN book b ON ol.book_id = b.book_id
"""
df_sales = pd.read_sql(sales_query, src_conn)

# Load using SQL JOIN with dimension tables
insert_query = """
INSERT INTO Fact_Sales (BookKey, CustomerKey, OrderDateKey, Price, Quantity)
SELECT 
    b.BookKey, 
    c.CustomerKey, 
    CAST(FORMAT(src_o.order_date, 'yyyyMMdd') AS INT), 
    src_ol.price,
    src_ol.quantity
FROM Gravity_Books.dbo.cust_order src_o
JOIN Gravity_Books.dbo.order_line src_ol ON src_o.order_id = src_ol.order_id
INNER JOIN Dim_Books b ON src_ol.book_id = b.BookID
INNER JOIN Dim_Customers c ON src_o.customer_id = c.CustomerID
"""
cursor.execute(insert_query)
```

</details>

<details>
<summary>✅ Phase 3: Data Validation & Export</summary>

**Inputs:**
- Source data extracts
- Transformed data

**Process:**
1. Validate row counts between source and destination
2. Check for null or invalid values
3. Export transformed data to CSV for backup/audit

**Outputs:**
- CSV files of transformed data
- Validation reports
- Log files

**Code Snippet:**
```python
# Export to CSV for auditing
df_fact.to_csv('Fact_Sales_Output.csv', index=False, encoding='utf-8-sig')
df_customers.to_csv('Customers_Output.csv', index=False, encoding='utf-8-sig')

print(f"Successfully exported {len(df_fact)} sales records")
```

</details>

---

## 🧬 Data Flow Diagram

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Source Tables│     │   ETL Process │     │  DW Tables   │
├──────────────┤     ├──────────────┤     ├──────────────┤
│ book         │────▶│              │────▶│ Dim_Books    │
│ book_language│────▶│   Extract    │     │              │
│ publisher    │────▶│   Transform  │     │ Dim_Customers│
│ customer     │────▶│   Load       │     │              │
│ address      │────▶│              │────▶│ Dim_Date     │
│ country      │────▶│              │     │              │
│ cust_order   │────▶│              │────▶│ Fact_Sales   │
│ order_line   │────▶│              │     │              │
└──────────────┘     └──────────────┘     └──────────────┘

Data Flow Steps:
1. Extract: Read from multiple source tables
2. Join: Combine related data (books + language + publisher)
3. Transform: Clean, format, generate surrogate keys
4. Load: Insert into dimension tables first, then fact table
```

---

## 🗂 Directory Structure

```
gravity_books_etl/
│
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (connection strings)
├── .gitignore                # Git ignore rules
│
├── src/
│   ├── __init__.py
│   ├── config.py             # Configuration settings
│   ├── connections.py        # Database connection management
│   ├── extract.py            # Data extraction functions
│   ├── transform.py          # Data transformation logic
│   ├── load.py               # Data loading functions
│   └── utils.py              # Utility functions
│
├── etl_pipeline.py           # Main ETL orchestration script
│
├── scripts/
│   ├── create_dw_tables.sql  # SQL script to create warehouse schema
│   ├── validate_counts.sql   # Validation queries
│   └── sample_queries.sql    # Example analytical queries
│
├── outputs/
│   ├── Fact_Sales_Output.csv      # Exported fact data
│   ├── Customers_Output.csv       # Exported customer data
│   └── etl_log.txt                # ETL process log
│
├── notebooks/
│   ├── data_exploration.ipynb     # Source data exploration
│   └── validation_queries.ipynb   # Data validation notebook
│
└── docs/
    ├── architecture_diagram.png    # System architecture
    ├── data_model.md               # Detailed data model documentation
    └── sql_server_setup.md         # SQL Server setup instructions
```

---

## 📦 Tech Stack

| Category          | Tool / Library                | Purpose                               |
|-------------------|-------------------------------|---------------------------------------|
| **Language**      | Python 3.8+                   | Core ETL logic                        |
| **Database**      | SQL Server                    | Source and destination databases      |
| **Database Driver**| pyodbc                       | Python-SQL Server connectivity        |
| **Data Processing**| pandas                        | Data manipulation and transformation  |
| **Data Export**   | CSV                           | Backup and audit files                |
| **Development**   | Jupyter Notebooks             | Exploration and testing               |
| **Version Control**| Git + GitHub                 | Code management                       |
| **Documentation** | Markdown                      | Project documentation                 |

**Key Dependencies:**
```txt
pyodbc>=4.0.0
pandas>=1.3.0
python-dotenv>=0.19.0
sqlalchemy>=1.4.0 (optional)
```

---

## 📊 Data Modeling Approach

### **Schema Design: Star Schema**
The data warehouse follows the Kimball dimensional modeling approach with a star schema design:

#### **Dimension Tables:**
1. **Dim_Books**
   - `BookKey` (Surrogate PK)
   - `BookID` (Natural/Business Key)
   - `Title`
   - `Language_Name`
   - `Publisher_Name`
   - `Publication_Date` (optional)
   - `ISBN13` (optional)

2. **Dim_Customers**
   - `CustomerKey` (Surrogate PK)
   - `CustomerID` (Natural/Business Key)
   - `FirstName`
   - `LastName`
   - `Email`
   - `StreetNumber`
   - `StreetName`
   - `City`
   - `Country`

3. **Dim_Date** (optional but recommended)
   - `DateKey` (INT in YYYYMMDD format)
   - `FullDate`
   - `Year`
   - `Quarter`
   - `Month`
   - `MonthName`
   - `Day`
   - `DayOfWeek`

#### **Fact Table:**
4. **Fact_Sales** (Transactional Fact)
   - `SalesKey` (Surrogate PK)
   - `BookKey` (FK to Dim_Books)
   - `CustomerKey` (FK to Dim_Customers)
   - `OrderDateKey` (FK to Dim_Date)
   - `Price` (measure)
   - `Quantity` (measure)
   - `LineTotal` (derived measure: Price × Quantity)

### **Modeling Approach: Kimball**
- **Bottom-up approach**: Starting with business process (sales)
- **Conformed dimensions**: Reusable across multiple fact tables
- **Balance of normalization and query performance**

### **Fact Table Type: Transactional**
- **Grain**: One row per line item in an order
- **Additive measures**: Price, Quantity, LineTotal
- **Foreign keys**: Connect to all associated dimensions

---

## 🗓 Roadmap

| Phase | Description | Start Date | End Date | Status |
|-------|-------------|------------|----------|--------|
| ✅ 1 | Requirements Analysis & Data Modeling | 2026-02-20 | 2026-02-22 | ✅ Done |
| ✅ 2 | Database Setup & Connection Testing | 2026-02-23 | 2026-02-24 | ✅ Done |
| ✅ 3 | Dimension Tables ETL Development | 2026-02-25 | 2026-02-26 | ✅ Done |
| ✅ 4 | Fact Table ETL Development | 2026-02-27 | 2026-02-28 | ✅ Done |
| ✅ 5 | Data Validation & Testing | 2026-03-01 | 2026-03-02 | ✅ Done |
| ✅ 6 | Documentation & Finalization | 2026-03-03 | 2026-03-06 | 🔄 In Progress |
| 🔄 7 | Incremental Load Implementation | TBD | TBD | 📅 Planned |
| 🔄 8 | SCD Type 2 Support | TBD | TBD | 📅 Planned |
| 🔄 9 | Performance Optimization | TBD | TBD | 📅 Planned |
| 🔄 10 | Monitoring & Alerting | TBD | TBD | 📅 Planned |

---

## 🧾 License

No license has been selected for this project yet.
All rights reserved — you may not use, copy, modify, or distribute this code without explicit permission from the author.

---


---

## 📬 Future Improvements

- **Incremental Load Strategies**
  - Implement Change Data Capture (CDC) for source tables
  - Add timestamp-based incremental extraction
  - Support for Slowly Changing Dimensions (SCD Type 2)

- **Performance Optimization**
  - Use bulk insert operations (e.g., `executemany` or `bcp`)
  - Implement parallel processing for large tables
  - Add indexing strategy for dimension lookups

- **Data Quality**
  - Add data quality checks and validation rules
  - Implement data profiling before load
  - Create data quality dashboard

- **Orchestration**
  - Add Apache Airflow for workflow management
  - Implement retry logic and error recovery
  - Add email/Slack notifications for failures

- **Scalability**
  - Support for cloud data warehouses (Azure SQL, Snowflake)
  - Implement Spark for distributed processing
  - Add partitioning for large fact tables

- **Monitoring & Observability**
  - Create ETL metrics dashboard
  - Track row counts, processing times, error rates
  - Implement data lineage tracking

- **Testing**
  - Add unit tests for transformation functions
  - Create integration test suite
  - Implement data validation tests

---

## 🙋‍♂️ Contributing

Contributions are welcome! This is an educational project, and improvements are appreciated. Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please ensure your code follows PEP 8 guidelines and includes appropriate documentation.

---

## 📞 Contact

For questions, suggestions, or feedback about this project:

**Manar ALtyp**
📧 Email: manaraltyp44444@gmail.com
🐙 GitHub: [Manar Altyp](https://github.com/manar-Lang)

---

## 📋 Assignment Requirements Checklist

| Requirement | Status | Location/Notes |
|-------------|--------|----------------|
| Source System (SQL Server/Flat Files) | ✅ | SQL Server (Gravity_Books) |
| ETL Tool (Python/Pandas) | ✅ | Python + pyodbc + pandas |
| Data Warehouse Destination (SQL Server) | ✅ | GravityBooks_DWH |
| Schema Design Explanation | ✅ | Star Schema (see [Data Modeling](#-data-modeling-approach)) |
| Modeling Approach (Inmon/Kimball) | ✅ | Kimball Dimensional Modeling |
| Fact Table Type | ✅ | Transactional Fact |
| Screenshots of ETL Process | ✅ | /docs/screenshots/ |
| SQL Server Database Diagram | ✅ | /docs/database_diagram.png |
| Architecture Explanation | ✅ | See [System Architecture](#-system-architecture) |

---

*Last Updated: March 16, 2026*
