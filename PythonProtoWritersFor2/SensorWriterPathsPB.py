datapath = 'C:\\Users\\mitch\\Desktop\\ProtoDataFull\\'
olddp = 'C:\\Users\\mitch\\Desktop\\GyroFor2\\'


from os import listdir
import fnmatch
import dot_dataXYZ_pb2 as loc
import new_sensor_data_pb2 as sensor
from google.protobuf.internal.encoder import _VarintBytes

filenames = [f for f in listdir(olddp) if fnmatch.fnmatch(f, '*.txt')]



try:
    dotFile = open(datapath+'locationsForAccel.pbs', 'wb')
    sensorFile = open(datapath+'accel.pbs', 'wb')
    sequenceNum = 1
    for fn in filenames:
        last_seqn = -1
        ndot = 1
        sensorType = -1
        
        sensorData = None
        with open(olddp+'/'+fn,'r') as f:
            linesList = f.readlines()
            seqn = 1
            #Each sensor event is its own sensor reading, this is done because each sensor event has its own exact location
            #^ Every SensorReading must correspond to a location i.e. 1 to 1 correspondance with dotDataXYZ added and SensorEvent added
            for record in linesList:
                recordList =record.split(',')
                if(len(recordList) < 8):
                    print(len(recordList))
                else:
                    x, y = recordList[6], recordList[7]
                    #one dot here for every sensor event
                    dotDataXYZ = loc.DotReadingXYZ()
                    dotDataXYZ.dot_nr = ndot
                    dotDataXYZ.X = float(x)
                    dotDataXYZ.Y = float(y)
                    dotDataXYZ.Z = 1.4
                    dotFile.write(_VarintBytes(dotDataXYZ.ByteSize()))
                    dotFile.write(dotDataXYZ.SerializeToString())
                    if(recordList[0] == "ACCELEROMETER"):
                        sensorType = 1
                    elif(recordList[0] == "MAGNETIC_FIELD"):
                        sensorType == 2
                    elif(recordList[0] == "GYROSCOPE"):
                        sensorType == 4
                        
                    sensorData = sensor.SensorReading()
                    sensorData.sequence_nr = seqn
                    #Puts sensor reading in milliseconds as specified in the .proto file
                    sensorData.timestamp = int(recordList[1])//1000
                    sensorData.last_dot_nr = ndot
                    #Puts sensor event in nanoseconds as specified in the .proto file
                    sensorData.sensor_event.timestamp = int(recordList[1])*1000
                    sensorData.sensor_event.sensor_type = sensorType
                    sensorData.sensor_event.accuracy = int(recordList[2])
                    value = sensorData.sensor_event.values.value.append(float(recordList[3][1:]))
                    value = sensorData.sensor_event.values.value.append(float(recordList[4]))
                    value = sensorData.sensor_event.values.value.append(float(recordList[5][:len(recordList[5])-1]))

                    
                    seqn+=1            
                    ndot = ndot + 1
                    
                    #NOTE: Doing SensorEvent = sensorData.sensor_event.add() does not work
                    sensorFile.write(_VarintBytes(sensorData.ByteSize()))
                    sensorFile.write(sensorData.SerializeToString())
                
 
    dotFile.close()
    sensorFile.close()
except IOError as e: 
    print('file open/write error'+e)

