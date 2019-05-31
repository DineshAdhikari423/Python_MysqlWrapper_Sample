import MySQLdb
import sys
from collections import OrderedDict


class MysqlWrapper(object):
    """
    This class helps to connect with MySQL server to
    do all CURD operations SELECT (with conditions),
    INSERT, UPDATE, DELETE.
    """
    __instance = None
    __host = None
    __user = None
    __password = None
    __database = None
    __session = None
    __connection = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance or not cls.__database:
            cls.__instance = super(MysqlWrapper, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self, host='localhost', user='root', password='', database=''):
        self.__host = host
        self.__user = user
        self.__password = password
        self.__database = database

    def __open(self):
        try:
            connection = MySQLdb.connect(self.__host, self.__user, self.__password, self.__database)
            self.__connection = connection
            self.__session = connection.cursor()
        except MySQLdb.Error:
            print "Error in connection"

    def __close(self):
        self.__session.close()
        self.__connection.close()

    def select(self, table, where=None, *args, **kwargs):
        query = 'SELECT '
        keys = args
        values = tuple(kwargs.values())
        l = len(keys) - 1

        for i, key in enumerate(keys):
            query += "`"+key+"`"
            if i < l:
                query += ","

        query += 'FROM %s' % table

        if where:
            query += " WHERE %s" % where

        self.__open()
        self.__session.execute(query, values)
        number_rows = self.__session.rowcount
        number_columns = len(self.__session.description)

        if number_rows >= 1 and number_columns > 1:
            result = [item for item in self.__session.fetchall()]
        else:
            result = [item[0] for item in self.__session.fetchall()]
        self.__close()

        return result

    def update(self, table, where=None, *args, **kwargs):
        query = "UPDATE %s SET " % table
        keys = kwargs.keys()
        values = tuple(kwargs.values()) + tuple(args)
        l = len(keys) - 1
        for i, key in enumerate(keys):
            query += "`"+key+"` = %s"
            if i < l:
                query += ","
            # End if i less than 1
        # End for keys
        query += " WHERE %s" % where

        self.__open()
        self.__session.execute(query, values)
        self.__connection.commit()

        # Obtain rows affected
        update_rows = self.__session.rowcount
        self.__close()

        return update_rows

    def insert(self, table, *args, **kwargs):
        values = None
        query = "INSERT INTO %s" % table
        if kwargs:
            keys = kwargs.keys()
            values = tuple(kwargs.values())
            query += "(" + ",".join(["`%s`"] * len(keys)) % tuple(keys) + ") VALUES (" + ",".join(["%s"]*len(values)) + ")"
        elif args:
            values = args
            query += " VALUES(" + ",".join(["%s"]*len(values)) + ")"

        self.__open()
        self.__session.execute(query, values)
        self.__connection.commit()
        self.__close()
        return self.__session.lastrowid

    def delete(self, table, where=None, *args):
        query = "DELETE FROM %s" % table
        if where:
            query += ' WHERE %s' % where

        values = tuple(args)

        self.__open()
        self.__session.execute(query, values)
        self.__connection.commit()

        # Obtain rows affected
        delete_rows = self.__session.rowcount
        self.__close()

        return delete_rows


def main():
    connect_mysql = MysqlWrapper('host.ip.address', 'user', 'password', 'database')
    conditional_query = 'emp_type = %s '
    result = connect_mysql.select('employee', conditional_query, 'id', 'emp_type', emp_type='contractor')
    # insert
    result = connect_msyql.insert('employee', emp_type='full_time', emp_code='EMP250')
    # update
    conditional_query = 'emp_type = %s'
    result = connect_mysql.update('employee', conditional_query, 'contractor', emp_level='55')
