import os

def getCSVofDB(dbname,tbname,csvFile):
    flag=0
    import csv
    from application.MySQLfacer import MySQLdb

    sqlApp=MySQLdb()
    sqlApp.setConfig('Sushil123','Sushil@123','localhost','')
    sqlApp.connectToMySQL()
    sqlApp.usedb(dbname)
    print("csvFile:",csvFile)

    describeTB=sqlApp.describetable(dbname,tbname)
    fields = [describeTB[i].split('\t')[0] for i in range(1,len(describeTB))]
    SQLdata=sqlApp.showAllTableDataFetchall(dbname,tbname)
    sqlApp.disconnectMySQL()

    with open(csvFile,'w') as CSVfile:
        writer=csv.writer(CSVfile)
        writer.writerow(fields)
        writer.writerows(SQLdata)
    CSVfile.close()
    flag=1

    return flag



def allFilesFromDirWithDateSize(dir):
    import os
    import time
    from datetime import datetime

    #allfilesFolders=os.listdir(path='.')    
    onlyfiles=[entry for entry in os.listdir(dir) if os.path.isfile(os.path.join(dir, entry))]
    onlyfilesFullPath=[os.path.join(dir,file) for file in onlyfiles]
    print(onlyfiles)
    print(onlyfilesFullPath)

    fileDetails=[]
    for file in onlyfiles:
        file_stats = os.stat(os.path.join(dir,file))
        mb='File Size :{:.2f} MB'.format(file_stats.st_size/(1024*1024))
        kb='{} KB'.format(float(file_stats.st_size/1024))
        b='{} B'.format(file_stats.st_size)
        modified_time=time.strftime("%d %b %Y %H:%M:%S", time.strptime(time.ctime(os.path.getmtime(os.path.join(dir,file)))))
        fileDetails.append('{} -size:{} -last modified:{}'.format(file,kb,modified_time))
    print(fileDetails)

    # for f in allFilesFromDirWithDateSize('./allCSV/'):
    # print(f)

    return fileDetails

def sessionId_to_ddmmyyyy(sid):
    '''return date in dd-mm-yyyy'''
    return '{}-{}-{}'.format(sid[0:-7],sid[-7:-5],sid[-5:-1])

def generateFinalReport(csvFile,monthYear=None):
    import csv
    from application.MySQLfacer import MySQLdb
    from application.csvUtilities import getDictToCSV

    sqlApp=MySQLdb()
    sqlApp.setConfig('Sushil123','Sushil@123','localhost','facerdb')
    con_status=sqlApp.connectToMySQL()
    sqlApp.usedb(dbname='facerdb')
    totalsessionIDs=list()

    List_attendanceDict=list()
    noColFetch=0
    print("generateFinalReport:",csvFile)

    if (monthYear != None):
        # list of session ids
        tempcursor,tempresult=sqlApp.UserQuery(query='select sessionId from sessionInfo')
        totalsessionIDs=[e[0] for e in tempresult]
        print("LIST_SESSIONS:-",totalsessionIDs)
        # list of staff name,staff id
        tempcursor,tempresult=sqlApp.UserQuery(query='select sid,sname from staffInfo')
        list_staffname=[e[1] for e in tempresult]
        print("LIST_STAFFNAME:-",list_staffname)
        print(os.getcwd())

        for staffname in list_staffname:
            attendanceQuery="select ss.sessionId as conducted ,if(ss.sessionId in (select a.sessionId from attendance a where a.sname='{}'),'P','A') as attended from sessionInfo ss where sessionId like '{}'".format(staffname,monthYear)
            tempcursor,tempresult=sqlApp.UserQuery(query=attendanceQuery)
            print("STAFFNAME:",staffname,tempresult)
            if (len(tempresult)==0):
                noColFetch=1

            if not(noColFetch):
                attendanceDict=dict()
                attendanceDict['sname']=staffname

                percentage=0

                for tupledata in tempresult:
                    temp = str(tupledata[0])
                    if len(temp) == 8:
                        temp = "0" + temp
                    attendanceDict[sessionId_to_ddmmyyyy(temp)]=tupledata[1]
                    if(tupledata[1]=='P'):
                        percentage+=1

            # add percentage key = value :remainig
            if not(noColFetch):
                attendanceDict['TotalAttendance']=round((percentage/len(tempresult))*100,2)

                print(attendanceDict)
                List_attendanceDict.append(attendanceDict)

                getDictToCSV(DictList=List_attendanceDict,csv_file=csvFile)
            else:
                return "No Columns Fetch to generate CSV"    

    sqlApp.disconnectMySQL()


if __name__ == '__main__':
    # getCSVofDB('facerdb','attendance','./static/allCSV/attendance.csv')
    # getCSVofDB('facerdb','sessionInfo','./static/allCSV/sessionInfo.csv')
    # getCSVofDB('facerdb','staffInfo','./static/allCSV/staffInfo.csv')

    for f in allFilesFromDirWithDateSize('./static/allCSV/'):
        print(f)

    generateFinalReport(csvFile='./static/allCSV/finalReport.csv')



'''
    select ss.sessionId as conducted ,
    if(ss.sessionId in (select a.sessionId from attendance a where a.sname='sushil'),'P','A') 
    as attended 
    from sessionInfo ss where sessionId like "%0120210" ;



    name date
    sushil 20032021 P
'''


