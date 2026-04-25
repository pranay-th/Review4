Project Overview:
This project demonstrates PostgreSQL concepts including DDL, DML, Functions,
Triggers, Joins, and Aggregations. It simulates a system for managing vessel
trade data, country information, and logging system activities.

------------------------------------------------------------
Tables Used:

1. vessels  
   Stores vessel-related data including toll charges.

2. logs_table  
   Stores logs with message and timestamp.

3. countryinfo  
   Stores country name and commodity.

4. country_summary  
   Stores aggregated trade data.

5. trade_records and cargo  
   Used for JOIN operations.

------------------------------------------------------------
Features Implemented:

1. Aggregation Function

Function Name: countcost()  
Purpose: Calculates total toll cost from vessels table.

CREATE OR REPLACE FUNCTION countcost()
RETURNS INT AS $$
BEGIN
  RETURN (SELECT SUM(toll_usd) FROM vessels);
END;
$$ LANGUAGE plpgsql;

Usage:
SELECT countcost();

------------------------------------------------------------
2. Trigger on countryinfo Table

CREATE OR REPLACE FUNCTION log_country_insert_func()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO logs_table(message, "timestamp")
  VALUES ('Inserted new country ' || NEW.name, NOW());
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_log_country_insert
AFTER INSERT ON countryinfo
FOR EACH ROW
EXECUTE FUNCTION log_country_insert_func();

------------------------------------------------------------
3. Insert Operation

INSERT INTO countryinfo (name, commodity)
VALUES ('INDIA', 'CRUDE OIL');

------------------------------------------------------------
4. JOIN Query

SELECT t.flag, c.commodity
FROM trade_records AS t
INNER JOIN cargo AS c
ON t.vessel_id = c.vessel_id;

------------------------------------------------------------
5. Trigger on country_summary Table

CREATE OR REPLACE FUNCTION log_country_summary_insert()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO logs_table(message, "timestamp")
  VALUES ('Summary updated for flag ' || NEW.flag, NOW());
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_log_country_summary
AFTER INSERT ON country_summary
FOR EACH ROW
EXECUTE FUNCTION log_country_summary_insert();

------------------------------------------------------------
6. Insert into country_summary

INSERT INTO country_summary (
  flag,
  total_trade_volume_usd,
  total_trades,
  average_trade_value_usd,
  commodities,
  date
)
VALUES (
  'INDIA',
  1000000,
  10,
  100000,
  'CRUDE OIL',
  NOW()
);

------------------------------------------------------------
Logs Verification:

SELECT * FROM logs_table;

How to Run:

1. Create all required tables
2. Run functions
3. Create triggers
4. Insert data
5. Execute queries

Concepts Covered:

- DDL (CREATE TABLE)
- DML (INSERT)
- Functions (PL/pgSQL)
- Triggers (AFTER INSERT)
- Aggregation (SUM)
- INNER JOIN
- Logging system

Future Improvements:

- Add UPDATE and DELETE triggers
- Add indexing
- Connect with Node.js backend
- Deploy on cloud (Neon)

