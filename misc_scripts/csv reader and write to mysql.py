import mysql.connector as mysqlcon
import csv

HOST = "localhost"
USERNAME = "root"
PASSWORD = "password"
DATABASE = "abcd"
l = []
inc = []
fname = "xyz.csv"
tname = "abcd"
noscol = 12


def sql_run(*sql_query):
    output = []
    sql_connection = None
    try:
        sql_connection = mysqlcon.connect(host=HOST, user=USERNAME, passwd=PASSWORD)
        cursor = sql_connection.cursor()
        sql_query = list(sql_query)
        sql_query.insert(0, ["Create database if not exists " + DATABASE + ";", ()])
        sql_query.insert(1, ["Use " + DATABASE + ";", ()])
        for l in sql_query:
            if isinstance(l, list) or isinstance(l, tuple):
                if len(l) == 2:
                    query, val = l
                else:
                    query = l[0]
                    val = ()
            else:
                query = l
                val = ()
            cursor.execute(query, val)
            if query.upper().startswith(("SELECT", "DESC", "SHOW")):
                output.append(cursor.fetchall())
            else:
                sql_connection.commit()
                output.append([])
        cursor.close()
        return output[2:]
    except (mysqlcon.Error, mysqlcon.Warning) as error:
        if error.errno == 2003:
            ermsg = "Failed to make a connection to the server."
            print(ermsg, "You are Offline!\n" + ermsg + "\nError Code : 2003")
        else:
            print("Error", error, sql_query)

    finally:
        if sql_connection:
            sql_connection.close()


def insertSQL(table, values):
    query = "Insert into {0} values(".format(table)
    for val in values:
        if isinstance(val, int) or isinstance(val, float):
            query += str(val) + ","
        else:
            query += "'" + val + "',"
    query = query[: len(query) - 1] + ");"
    return sql_run(query)


# Main Program

with open(fname) as fh:
    creader = csv.reader(fh)
    for rec in creader:
        if len(rec) == noscol:
            insertSQL(tname, rec)
        else:
            inc.append(rec)

print("Incorrect data in file :", inc)
