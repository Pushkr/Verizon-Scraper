--Use this script to load hive tables 

-- create managed database
CREATE DATABASE IF NOT EXISTS verizon;


set hive.exec.dynamic.partition.mode=nonstrict;
set hive.exec.dynamic.partition.mode;


CREATE  TABLE IF NOT EXISTS ${hiveconf:TABLE}
   (word STRING,
    count BIGINT)
  PARTITIONED BY (DATE STRING,HOUR STRING)
  ROW FORMAT DELIMITED
  FIELDS TERMINATED BY ','
  LINES TERMINATED BY '\n';

--describe formatted ${hiveconf:TABLE} ;



create temporary table test_data (
    tword string,
    tcnt bigint
    )
row format DELIMITED
fields terminated by ","
lines terminated by "\n"
location '${hiveconf:LCTN}';

FROM test_data
INSERT INTO ${hiveconf:TABLE} PARTITION (DATE,HOUR)
SELECT TWORD, TCNT, current_date as DATE, hour(current_timestamp) as HOUR;



--perform tests

--describe formatted ${hiveconf:TABLE} ;

--select * from ${hiveconf:TABLE} LIMIT 2;

