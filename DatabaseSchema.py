from BakeryManagementSystem.db import c,conn
from time import strftime
user_table_query ="""
CREATE TABLE IF NOT EXISTS user(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    joiningDate CHAR(10),
    name CHAR(50),
    username CHAR(50),
    password CHAR(50),
    email CHAR(40),
    address CHAR(70),
    phone CHAR(40),
    cnic CHAR(20),
    status CHAR(10)
)
""" 
c.execute(user_table_query)
category_table_query ="""
CREATE TABLE IF NOT EXISTS category(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name CHAR(70)
)
""" 
c.execute(category_table_query)
item_table_query ="""
CREATE TABLE IF NOT EXISTS items(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date_time CHAR(20),
    item_name CHAR(70),
    weight INTEGER,
    quantity INTEGER,
    category_id INTEGER,
    price INTEGER,
    expire_date CHAR(10),
    FOREIGN KEY(category_id) REFERENCES category(id)
)
""" 
c.execute(item_table_query)
invoices_table_query ="""
CREATE TABLE IF NOT EXISTS invoices(
    number INTEGER,
    date_time CHAR(20),
    item_id INTEGER,
    item_name CHAR(70),
    quantity INTEGER,
    price INTEGER,
    status CHAR(10),
    FOREIGN KEY(item_id) REFERENCES items(id)
)
""" 
c.execute(invoices_table_query)
c.execute(f"INSERT INTO user(joiningDate,name,username,password,email,address,phone,cnic,status) VALUES('{strftime('%d-%m-%Y')}','admin','admin','admin*','admin@admin.com','Users address','0300000000','00000-00000000-0','admin')")
conn.commit()
