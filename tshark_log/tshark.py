
import twinlooper
from hexdump import hexdump

pedal = twinlooper.twinlooper()

dump = open("tshark.dump", "r")
lines = dump.readlines()
  
# Strips the newline character
for line in lines:
    text = line[37:-4:].replace(":", "" )
    test = bytes.fromhex(text)

    print(line[0:80])
    print(hexdump(pedal.unpack(test)[:64]))
    print()
    
