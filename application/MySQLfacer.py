#MySQL SetUp Codes
from mysql.connector import errorcode
import mysql.connector
class MySQLdb:
    def __init__(self):
        super(MySQLdb,self).__init__()
        self.config={
            'user': 'Sushil123',
            'password': 'Sushil@123',
            'host': '127.0.0.1',
            'database': 'facerdb',
            'raise_on_warnings': True
        }

        self.db_connection= None
        self.db_connectionId= None
        self.db_cursor= None

        self.db_databasesList = None
        self.db_tablesList = None

    #Getters
    def getConnection(self):
        return self.db_connection
    
    def getCursor(self):
        return self.db_cursor


    #Setters
    def setConfig(self,username='Sushil123',password='Sushil@123',host='localhost',database=''):
        self.config['user']=username
        self.config['password']=password
        self.config['host']=host
        if database !='':
            self.config['database']=database



    #Modules
    def connectToMySQL(self):
        try:
            self.db_connection=mysql.connector.connect(**self.config)
            #mysql.connector.connect(host=hostname,user=username,passwd=password)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
                print('ERROR:',str(err))
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print('handle this Error:',err)
        else:
            #severything is good

            if(self.db_connection):
                self.db_connectionId=self.db_connection.connection_id
                self.db_cursor=self.db_connection.cursor()
        return self.db_connectionId

    def disconnectMySQL(self):
        self.db_connection.close()

    def showdatabases(self):
        self.db_databasesList=[]
        self.db_cursor.execute("show databases")
        for cursor in self.db_cursor:
            self.db_databasesList.append(cursor[0])
        return self.db_databasesList

    def createdatabase(self,dbname):
        flag=0
        if dbname not in self.showdatabases():
            createdbQuery = "create database " + dbname
            self.db_cursor.execute(createdbQuery)
            self.db_connection.commit()
            #print("Database created Successfully :" + dbname)
            self.showdatabases()
            flag=1
        return flag

    def dropdatabase(self,dbname):
        flag=0
        if dbname in self.showdatabases():
            dropdbQuery = "drop database " + dbname
            self.db_cursor.execute(dropdbQuery)
            self.db_connection.commit()
            flag=1
        return flag

    def usedb(self,dbname):
        flag=0
        if dbname in self.showdatabases():
            usedbQuery = "use " + dbname
            self.db_cursor.execute(usedbQuery)
            self.db_connection.commit()
            flag=1
        return flag

    def showtables(self,dbname):
        self.db_tablesList=[]
        if dbname in self.showdatabases():
            self.db_cursor.execute("show tables")
            for cursor in self.db_cursor:
                self.db_tablesList.append(cursor[0])
        return self.db_tablesList

    def createtable(self,dbname,tbname,columnDataType):
        flag=0
        if dbname in self.showdatabases():
            if tbname not in self.showtables(dbname):
                createtbQuery = "create table " + tbname + "(" + columnDataType + ")"
                #print(createtbQuery)
                self.db_cursor.execute(createtbQuery)
                self.db_connection.commit()
                #print("table created Successfully : " + tbname)
                #if tbname in self.showtables(dbname):
                flag=1
        return flag

    def describetable(self,dbname,tbname):
        tableDescription=[]
        if dbname in self.showdatabases():
            if tbname in self.showtables(dbname):
                describetbQuery = "describe " + tbname
                #print("Description of : " + tbname + " is as follows:\n")
                self.db_cursor.execute(describetbQuery)
                #print("Field Type Null Default")
                tableDescription.append("Field\tType\tNull\tDefault")
                for cursor in self.db_cursor:
                    tableDescription.append("{}\t{}\t{}\t{}".format(cursor[0], cursor[1], cursor[2], cursor[4]))
        return tableDescription

    def insertInTable(self,dbname,tbname,DataValues):
        flag=0
        if dbname in self.showdatabases():
            if tbname in self.showtables(dbname):
                #describetb(tablename)
                InsertintbQuery = "insert into " + tbname + " values(" + DataValues + ")"
                self.db_cursor.execute(InsertintbQuery)
                self.db_connection.commit()
                #print("Data Inserted in " + tbname + "\n")
                flag=1
        return flag

    def showAllTableData(self,dbname,tbname):
        tableDataList=[]
        tableDataListOfTuples=[]
        if dbname in self.showdatabases():
            if tbname in self.showtables(dbname):
                print("Data in table : " + tbname)
                showdatatbQuery = "select * from " + tbname
                self.db_cursor.execute(showdatatbQuery)
                for cursor in self.db_cursor:
                    tableDataList.append("{} {}".format(cursor[0], cursor[1]))
                    tableDataListOfTuples.append("{},{}".format(cursor[0], cursor[1]))
        return tableDataList

    def showAllTableDataFetchall(self,dbname,tbname):
        if dbname in self.showdatabases():
            if tbname in self.showtables(dbname):
                #print("Data in table : " + tbname)
                showdatatbQuery = "select * from " + tbname
                self.db_cursor.execute(showdatatbQuery)
        return self.db_cursor.fetchall()

    def droptable(self,dbname,tbname):
        flag=0
        if dbname in self.showdatabases():
            if tbname in self.showtables(dbname):
                if(self.usedb(dbname)):
                    droptbQuery="DROP TABLE IF EXISTS "+tbname
                    self.db_cursor.execute(droptbQuery)
                    flag=1
        return flag

    def UserQuery(self,query,autocommit=1):
        if(autocommit):
            self.db_connection.autocommit=True
        uQuery = query

        self.db_cursor.execute(uQuery)
        return self.db_cursor,self.db_cursor.fetchall()

def tryMain():
    sqlApp=MySQLdb()

    sqlApp.setConfig('Sushil123','Sushil@123','localhost','facerdb')

    con_status=sqlApp.connectToMySQL()
    if(con_status>0):
        print('1. Connected Successfully at ConnectionId :'+str(con_status))
    print('Databases :',sqlApp.showdatabases())

    if(sqlApp.createdatabase('testdb')):
        print('2. Created testdb database :',sqlApp.showdatabases())

    if(sqlApp.usedb('testdb')):
        print('3. Database Selected')

    print('4. Tables in testdb:',sqlApp.showtables('testdb'))

    if(sqlApp.createtable('testdb', 'BE', str("ID int, Name varchar(20)"))):
        print("5. Created Table")
        print("Table List\n", sqlApp.showtables('testdb'))
        print("6. Table Description \n", sqlApp.describetable('testdb', 'BE'))

    if(sqlApp.insertInTable('testdb', 'BE', "1 ,'Akash'")):
        print("7. Data Inserted")
    print(sqlApp.UserQuery(query="insert into BE values(2,'Jaid')")[1])

    print("8. Table Data \n",sqlApp.showAllTableData('testdb', 'BE'))

    if(sqlApp.droptable('testdb','BE')):
        print("9. Table Dropped")
        print("Table List\n", sqlApp.showtables('testdb'))

    if(sqlApp.dropdatabase('testdb')):
        print("10. Database deleted")  

    print(sqlApp.UserQuery(query='show databases')[1])

    sqlApp.disconnectMySQL()
    print('MySQL disconnected')

if __name__ == '__main__':
    # tryMain()
    pass
