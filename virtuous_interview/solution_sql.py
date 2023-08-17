# AUTOGENERATED! DO NOT EDIT! File to edit: ../01_SQL_Solution.ipynb.

# %% auto 0
__all__ = ['DB_NAME', 'engine', 'tables', 'add_column', 'insert_contact_type', 'update_zip', 'update_deceased', 'update_gift_type', 'proc', 'insert_sql', 'insert_proc']

# %% ../01_SQL_Solution.ipynb 2
import pandas as pd
import mysql.connector

from .utils import contacts, contact_methods, gifts
from mysql.connector import Error
from dotenv import dotenv_values
from sqlalchemy import create_engine

# %% ../01_SQL_Solution.ipynb 5
DB_NAME = 'exam_db'

# %% ../01_SQL_Solution.ipynb 17
engine = create_engine(f'mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@localhost/{DB_NAME}')

# %% ../01_SQL_Solution.ipynb 7
try:
    connection = mysql.connector.connect(user='root', host='localhost')
    cursor = connection.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME};")
except Error as e:
    print(f"Error: {e}")
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()


# %% ../01_SQL_Solution.ipynb 11
def insert_sql(sql):
    try:
        # Connect to MySQL
        connection = mysql.connector.connect(user=DB_USER, password=DB_PASSWORD, host='localhost', database=DB_NAME)
        cursor = connection.cursor()
    
        # Execute the SQL command to create the view
        cursor.execute(sql)
        print("SQL executed successfully")
    
    except Error as e:
        print(f"Error: {e}")
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
        print("MySQL connection closed")

# %% ../01_SQL_Solution.ipynb 13
def insert_proc(sql, proc_name, call=True):
    insert_sql(f'DROP PROCEDURE IF EXISTS {proc_name};')
    stmt = f"""         
        CREATE PROCEDURE {proc_name}()
        BEGIN
            {sql}
        END;
        COMMIT;
    """
    insert_sql(stmt)
    if call:
        insert_sql(f'CALL {proc_name}();')

# %% ../01_SQL_Solution.ipynb 16
tables = {'temp_contact_methods': contact_methods, 'temp_contacts': contacts, 'temp_gifts': gifts}

# %% ../01_SQL_Solution.ipynb 18
try:
    for table_name, df in tables.items():
        try:
            df.to_sql(table_name, engine, index=False, if_exists='fail')
        except ValueError:
            print(f"Table {table_name} already exists. Skipping.")

except Error as e:
    print(f"Error: {e}")

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()


# %% ../01_SQL_Solution.ipynb 25
add_column = """
    DROP PROCEDURE IF EXISTS add_column;
    
    
    CREATE PROCEDURE add_column(
        IN tableName VARCHAR(255),
        IN columnName VARCHAR(255),
        IN columnType VARCHAR(255)
    )
    BEGIN
        DECLARE columnExists BOOLEAN DEFAULT FALSE;
    
        SELECT COUNT(*)
        INTO columnExists
        FROM information_schema.COLUMNS
        WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = tableName AND COLUMN_NAME = columnName;
    
        IF columnExists = 0 THEN
            SET @sql = CONCAT('ALTER TABLE ', tableName, ' ADD COLUMN ', columnName, ' ', columnType);
            PREPARE stmt FROM @sql;
            EXECUTE stmt;
            DEALLOCATE PREPARE stmt;
        END IF;
        COMMIT;
    END;
"""
insert_sql(add_column)

# %% ../01_SQL_Solution.ipynb 26
insert_contact_type = """
    CALL add_column('temp_contacts', 'ContactType', 'VARCHAR(255)');
    
    UPDATE temp_contacts
    SET ContactType = CASE WHEN CompanyName = '' THEN 'Household' ELSE 'Organization' END;
    COMMIT;
"""
insert_proc(insert_contact_type, 'insert_contact_type', call=True)

# %% ../01_SQL_Solution.ipynb 33
update_zip = """
    UPDATE temp_contacts
    SET Postal = ''
    WHERE Postal NOT REGEXP '^[0-9]{5}$' AND Postal NOT REGEXP '^[0-9]{5}-[0-9]{4}$';
    COMMIT;
"""
insert_proc(update_zip, 'update_zip', call=True)

# %% ../01_SQL_Solution.ipynb 35
update_deceased = f"""
    UPDATE temp_contacts
    SET Deceased = CASE
        WHEN Deceased = 'Yes' THEN 1
        ELSE 0
    END;
    commit;
    ALTER TABLE temp_contacts MODIFY Deceased TINYINT;
    commit;
"""
insert_proc(update_deceased, 'update_deceased', call=True)

# %% ../01_SQL_Solution.ipynb 39
update_gift_type = f"""
  UPDATE temp_gifts
  SET PaymentMethod = CASE
    WHEN AmountReceived < 0 THEN 'Reversing Transaction'
    WHEN LOWER(TRIM(PaymentMethod)) = 'cash' THEN 'Cash'
    WHEN LOWER(TRIM(PaymentMethod)) = 'check' THEN 'Check'
    WHEN LOWER(TRIM(PaymentMethod)) LIKE 'credit%' THEN 'Credit'
    ELSE 'Other'
  END;
  commit;
"""
insert_proc(update_gift_type, 'update_gift_type', call=True)

# %% ../01_SQL_Solution.ipynb 42
proc = f"""
UPDATE temp_gifts
    SET CreditCardType = CASE
    WHEN CreditCardType  = 'Master card' THEN 'Mastercard'
    else 'AMEX'
    end
WHERE CreditCardType IN ('American Ex', 'Master car');
commit;
"""
insert_proc(proc, 'update_gift_type', call=True)

# %% ../01_SQL_Solution.ipynb 50
proc = """
CREATE TABLE IF NOT EXISTS contact_methods (
    `LegacyContactId` VARCHAR(255),
    `Type` VARCHAR(255),
    `Value` VARCHAR(255)
);

BEGIN
DECLARE done INT DEFAULT FALSE;
DECLARE v_LegacyContactId VARCHAR(255);
DECLARE v_HomePhone VARCHAR(255);
DECLARE v_HomeEmail VARCHAR(255);
DECLARE v_Phone VARCHAR(255);
DECLARE v_Email VARCHAR(255);
DECLARE v_Fax VARCHAR(255);
DECLARE cur CURSOR FOR 
    SELECT 
        temp_contacts.`Number` AS LegacyContactId,
        temp_contact_methods.`Phone` AS HomePhone,
        temp_contact_methods.`EMail` AS HomeEmail,
        temp_contacts.`Phone` AS Phone,
        temp_contacts.`EMail` AS Email,
        temp_contact_methods.Fax AS fax
    FROM 
        temp_contacts
    LEFT JOIN
        temp_contact_methods ON temp_contact_methods.DonorNumber = temp_contacts.`Number`;

DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

    OPEN cur;

    read_loop: LOOP
        FETCH cur INTO v_LegacyContactId, v_HomePhone, v_HomeEmail, v_Phone, v_Email, v_Fax;
        
        IF done THEN
            LEAVE read_loop;
        END IF;

        INSERT INTO contact_methods (`LegacyContactId`, `Type`, `Value`) VALUES 
            (v_LegacyContactId, 'HomePhone', v_HomePhone),
            (v_LegacyContactId, 'HomeEmail', v_HomeEmail),
            (v_LegacyContactId, 'HomePhone', v_Phone),
            (v_LegacyContactId, 'HomeEmail', v_Email),
            (v_LegacyContactId, 'Fax', v_Fax);
    END LOOP;

    CLOSE cur;
END;

-- Delete records from contact methods where value is null or ''
DELETE FROM contact_methods WHERE `Value` IS NULL OR `Value` = '';

CREATE TEMPORARY TABLE temp_contact_methods AS
SELECT DISTINCT LegacyContactId, Type, Value
FROM contact_methods;

DELETE FROM contact_methods;

INSERT INTO contact_methods (LegacyContactId, Type, Value)
SELECT DISTINCT LegacyContactId, Type, Value
FROM temp_contact_methods;

DROP TEMPORARY TABLE IF EXISTS temp_contact_methods;


commit;


"""
insert_proc(proc, 'transform_contact_methods', call=True)