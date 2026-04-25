SELECT* FROM vessels;
SELECT * FROM logs_table;


--aggretion+function
CREATE OR REPLACE FUNCTION countcost()
RETURNS INT AS $$
BEGIN
	 RETURN (SELECT sum(toll_usd) FROM vessels);
END;
$$ LANGUAGE plpgsql;


--DDL
CREATE TABLE countryinfo(
  id serial primary key,
  name varchar(50),
  commodity varchar(50),
  updated_at timestamp default NOW()
);


--TRIGGERS AND FUNCTION
CREATE OR REPLACE FUNCTION log_country_insert_func()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO logs_table(message, "timestamp")
  VALUES (
    'Inserted new country ' || NEW.name,
    NOW()
  );

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;
CREATE TRIGGER trg_log_country_insert
AFTER INSERT ON countryinfo
FOR EACH ROW
EXECUTE FUNCTION log_country_insert_func();

--DML
INSERT INTO countryinfo (name, commodity)
VALUES ('INDIA', 'CRUDE OIL');


--JOINS AND USING INNER JOIN TO FIND COMMAN
SELECT t.flag, c.commodity
FROM trade_records AS t
INNER JOIN cargo AS c
ON t.vessel_id = c.vessel_id;



CREATE OR REPLACE FUNCTION log_country_summary_insert()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO logs_table(message, "timestamp")
  VALUES (
    'Summary updated for flag ' || NEW.flag,
    NOW()
  );

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;
CREATE TRIGGER trg_log_country_summary
AFTER INSERT ON country_summary
FOR EACH ROW
EXECUTE FUNCTION log_country_summary_insert();

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



SELECT countcost();