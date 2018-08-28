import sys
sys.dont_write_bytecode = True
import dot_data_pb2
from google.protobuf.internal.encoder import _VarintBytes


datapath = 'C:\\Users\\mitch\\Desktop\\ProtoDataFull\\'


input_file = 'C:\\Users\\mitch\\Desktop\\StepTimeStampsFor1\\1535059536123.txt'
count = 0
dotFile = open(datapath+'Collection1Steps.pbs', 'wb')
entries = []
with open(input_file,'r') as finput:
    for line in finput:
        line = line.strip()
        attrs = line.split(',')
        stepsFor1 = dot_data_pb2.DotReading()
        stepsFor1.dot_nr = int(attrs[0])
        stepsFor1.timestamp = int(attrs[1])
        print(stepsFor1)
        dotFile.write(_VarintBytes(stepsFor1.ByteSize()))
        dotFile.write(stepsFor1.SerializeToString())
        count+=1
dotFile.close()






        
