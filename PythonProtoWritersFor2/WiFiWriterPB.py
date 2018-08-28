datapath = 'C:\\Users\\mitch\\Desktop\\ProtoDataFull\\'
olddp = 'C:\\Users\\mitch\\Desktop\\WiFiFor2\\'


from os import listdir
import fnmatch
import dot_dataXYZ_pb2 as loc
import wifi_data_pb2 as WiFi
from google.protobuf.internal.encoder import _VarintBytes

filenames = [f for f in listdir(olddp) if fnmatch.fnmatch(f, '*.txt')]

# filename X,Y.txt
# write X,Y into dot pbs


try:
    dotFile = open(datapath+'locationsForWifi.pbs', 'wb')
    wifiFile = open(datapath+'wifi.pbs', 'wb')
    
    for fn in filenames:
        #Each file has its own list of sequences
        #Each single AP scan (i.e. a line) has its own individual dot
        seqn = 1
        last_seqn = -1
        ndot = 1
        
        # wifi data is stored scan by scan
        # more info on how to handle repeated field can be found at https://developers.google.com/protocol-buffers/docs/reference/python-generated?csw=1#repeated-message-fields
        wifiData = None
        with open(olddp+'/'+fn,'r') as f:
            for record in f.readlines():
                recordList =record.split(',')
                seq = record.split(',')[0]
                x, y = recordList[7], recordList[8]
                dotDataXYZ = loc.DotReadingXYZ()
                dotDataXYZ.dot_nr = ndot
                dotDataXYZ.X = float(x)
                dotDataXYZ.Y = float(y)
                dotDataXYZ.Z = 1.4
                dotFile.write(_VarintBytes(dotDataXYZ.ByteSize()))
                dotFile.write(dotDataXYZ.SerializeToString())
       
                if int(seq) != last_seqn : 
                    if wifiData is not None:
                        seqn = seqn + 1
                        wifiFile.write(_VarintBytes(wifiData.ByteSize()))
                        wifiFile.write(wifiData.SerializeToString())
                        
                    wifiData = WiFi.WiFiReading()
                    wifiData.last_dot_nr = ndot #Each single scan has its own dot
                    wifiData.sequence_nr = seqn #Sequence number is the scan number
                    last_seqn = int(seq)
                    
                wifiAP = wifiData.wifi_ap.add()
                wifiAP.bssid = record.split(',')[1]
                wifiAP.rssi = int(record.split(',')[5])
                ndot = ndot + 1

        wifiFile.write(_VarintBytes(wifiData.ByteSize()))
        wifiFile.write(wifiData.SerializeToString())
 
    dotFile.close()
    wifiFile.close()
except IOError as e: 
    print('file open/write error'+e)


# write the wifi scans into WiFi pbs

