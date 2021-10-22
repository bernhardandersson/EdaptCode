import pymysql

hostname = "rds-edapt-uat.cg5bofaurksl.ap-southeast-2.rds.amazonaws.com"
username_db = "edapt-prod"
password_db = "MG3lmJ69Eqnb9EJu"
database = "edapt_ilp"

#Defining connection to Edapt UAT database
def make_EdaptUAT_conn():
    myConnection = pymysql.connect( host=hostname, user=username_db, passwd=password_db, db=database )
    return myConnection

#Closing connection to Edapt UAT database
def close_EdaptUAT_conn():
    myConnection.close()

#Queries query_string to database referred to by connection conn, returns results
def query(query_string, conn):
    cur = conn.cursor()
    cur.execute(query_string)
    return cur.fetchall()

#Returns all combinations of school and staff
def school_staff_query(conn):
    return query("select school_id, staff_id from tbl_school_staff", conn)