def getDictToCSV(Dict={},DictList=[],csv_file='./static/allCSV/temp-getDictToCSV.csv'):
    import csv
    status=0
    headers = []
    keysColumn = []
    print("checkpoint1")
    print(csv_file)
    if (Dict=={}) and not(DictList==[]):
        keysColumn=DictList[0].keys()
    elif not(Dict=={}) and (DictList==[]):
        # headers = ["Name"]
        # headers = headers + list(Dict.keys())[1:]
        keysColumn=list(Dict.keys())
        # print("HEADER OF CSV :",headers)
        # keysColumn = headers
    try:
        with open(csv_file, 'w') as csvfile:
            print("KEY-COLUMNS:",keysColumn,type(keysColumn))

            writer = csv.DictWriter(csvfile, fieldnames=keysColumn)
            writer.writeheader()

            if (Dict=={}) and not(DictList==[]):
                writer.writerows(DictList)
                status = 1
            elif not(Dict=={}) and (DictList==[]):
                writer.writerow(Dict)
                status = 1

    except IOError:
        print("I/O error")
    return status


def alterCSVHeader(csv_file='./static/allCSV/testDictList2CSV.csv',header=[]):
    import csv
    oldHeader=None
    csvRows = []
    print("checkpoint2")
    print(csv_file)

    with open(csv_file, "r") as csvfile:
        csvreader = csv.reader(csvfile)
        oldHeader = next(csvreader)        

        for row in csvreader:
            csvRows.append(row)

    with open(csv_file, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        if(len(oldHeader)==len(header)):
            csvwriter.writerow(header)
        csvwriter.writerows(csvRows)
    return {'oldHeader':oldHeader}

def getCSVheader(csv_file='./static/allCSV/testDictList2CSV.csv'):
    import csv
    print("checkpoint3")
    print(csv_file)
    with open(csv_file, "r") as csvfile:
        csvreader = csv.reader(csvfile)
        return next(csvreader) 


def convertDictToListOfList(csv_file='./static/allCSV/testDictList2CSV.csv'):
    import csv
    csvRows = []
    print("checkpoint444")
    print(csv_file)

    with open(csv_file, "r") as csvfile:
        csvreader = csv.reader(csvfile)       

        for row in csvreader:
            csvRows.append(row)
    return csvRows
