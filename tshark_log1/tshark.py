# Logs processed with:
#
# $ tshark -r log.pcapng -2 -R 'sysex' -T fields   -e usb.src -e usb.dst -e usbaudio.sysex.reassembled.data > log.txt

import twinlooper
from hexdump import hexdump

pedal = twinlooper.twinlooper()

dump = open("log.txt", "r")
lines = dump.readlines()
  
# Strips the newline character
for line in lines:
    text = line[37:-4:].replace(":", "" )
    test = bytes.fromhex(text)

    print(line[0:80])
    print(hexdump(pedal.unpack(test)[:64]))
    print()
    
