olddp = 'C:\\Users\\mitch\\Desktop\\WiFiFor2\\'

from os import listdir
import fnmatch

filenames = [f for f in listdir(olddp) if fnmatch.fnmatch(f, '*.txt')]

# filename X,Y.txt
# write X,Y into dot pbs


try:
    APList = []
    for fn in filenames:
        with open(olddp+'/'+fn,'r') as f:
            for record in f.readlines():
                records = record.split(',')
                if(len(APList)!=0):
                    sameEntry = False
                    for k in APList:
                        if(records[1] == k):
                            sameEntry = True
                    if(sameEntry == False):
                        APList.append(records[1])
                else:
                    APList.append(records[1])
    print(APList)
    fileOut = open('C:\\Users\\mitch\\Desktop\\APList.txt', 'w')
    for i in APList:
        fileOut.write(i + ",")
    fileOut.close()
 
except IOError as e: 
    print('file open/write error'+e)

