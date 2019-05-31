# Dependencies
============= 
* python version 2.7
* pip install MySQL-python

# Usage
======
"""
This class helps to connect with MySQL server to do all CURD operations
SELECT (with conditions), INSERT, UPDATE, DELETE.
"""

from MysqlWrapper import MyMysqlWrapper
connect_mysql = MysqlWrapper('host.ip.address', 'user', 'password', 'database')
conditional_query = 'emp_type = %s '
result = connect_mysql.select('employee', conditional_query, 'id', 'emp_type', emp_type='contractor')

# Insert
result = connect_msyql.insert('employee', emp_type='full_time', emp_code='EMP250')

# Update
conditional_query = 'emp_type = %s'
result = connect_mysql.update('employee', conditional_query, 'contractor', emp_level='55')

