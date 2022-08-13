#pip install mysql-connector-python
import mysql.connector
try:
    conn = mysql.connector.connect(host='localhost',user='Sushil123',passwd='Sushil@123'))
except mysql.connector.Error as err:
  
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
    print('ERROR:',str(err))
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:

    cursordb=conn.cursor()

    '''
        showdatabases
        create database
        use
        showtables
        create table
        describe
        select
        insert : commit
        update : commit
        delete : commit
        dropdb
        droptb
    '''

    #show databases
    cursordb.execute("show databases")

    #create database
    cursordb.execute("create database testdb")
    conn.commit()

    #use database
    cursordb.execute("use testdb")
    conn.commit()

    #show tables
    cursordb.execute("show tables")

    #create table
    cursordb.execute("create table tbname(ID int, Name varchar(20))")
    conn.commit()

    #descibe table

    #"Field\tType\tNull\tDefault"
    cursordb.execute("describe table tbname")

    #insert table
    cursordb.execute("insert into table values (1 ,'Akash')")
    conn.commit()

    DROP TABLE IF EXISTS 
    cursordb.execute("DROP TABLE IF EXISTS tbname")
    conn.commit()

    #drop database
    cursordb.execute("drop database testdb")
    conn.commit()

    conn.close()
