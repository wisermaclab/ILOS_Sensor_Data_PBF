datapath = 'C:\\Users\\mitch\\Desktop\\ProtoDataFull\\'
olddp = 'C:\\Users\\mitch\\Desktop\\AccelDataFor1\\'


from os import listdir
import fnmatch
import dot_dataXYZ_pb2 as loc
import new_sensor_data_pb2 as sensor
from google.protobuf.internal.encoder import _VarintBytes

filenames = [f for f in listdir(olddp) if fnmatch.fnmatch(f, '*.txt')]



try:
    sensorFile = open(datapath+'accelFor1.pbs', 'wb')
    sequenceNum = 1
    for fn in filenames:
        last_seqn = -1
        ndot = 1
        sensorType = -1
        
        sensorData = None
        with open(olddp+'/'+fn,'r') as f:
            linesList = f.readlines()
            seqn = 1
            for record in linesList:
                recordList =record.split(',')
                if(len(recordList) < 6):
                    print(len(recordList))
                else:
                    recordList[0] = recordList[0].capitalize()
                    if(recordList[0] == "ACCELEROMETER"):
                        sensorType = 1
                    elif(recordList[0] == "MAGNETIC_FIELD"):
                        sensorType == 2
                    elif(recordList[0] == "GYROSCOPE"):
                        sensorType == 4
                        
                    sensorData = sensor.SensorReading()
                    sensorData.sequence_nr = seqn
                    #puts sensor timestamp in milliseconds as specified in the .proto file
                    sensorData.timestamp = int(recordList[1])
                    sensorData.last_dot_nr = ndot
                    #puts event timestamp in nanoseconds as specified in the .proto file
                    sensorData.sensor_event.timestamp = int(recordList[1])*1000000
                    sensorData.sensor_event.sensor_type = sensorType
                    sensorData.sensor_event.accuracy = int(recordList[2])
                    
                    value = sensorData.sensor_event.values.value.append(float(recordList[3][1:]))
                    value = sensorData.sensor_event.values.value.append(float(recordList[4]))
                    value = sensorData.sensor_event.values.value.append(float(recordList[5][:len(recordList[5])-2]))

                    
                    seqn+=1            
                    ndot = ndot + 1
                    
                    #NOTE: Doing SensorEvent = sensorData.sensor_event.add() does not work
                    sensorFile.write(_VarintBytes(sensorData.ByteSize()))
                    sensorFile.write(sensorData.SerializeToString())
                
 
    sensorFile.close()
except IOError as e: 
    print('file open/write error'+e)
