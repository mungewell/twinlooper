from hexdump import hexdump

infile = open("info.bin", "rb")

# why limit to this length?
info = infile.read(0x0bd3)

print("Header:")
print(hexdump(info[:32]))
print()

# base start at 0x00000010, up to where '00 00' or 'FF FF'
# 
# the whole 10mins loop has 649 items, this means 0.92449923s per item
# 0.92449923 * 48KHz * 2 * 3 = 266255.77 bytes per item...
# (0x03F1) * 4 + 0x38 = 4092 bytes per block 
#              -> 64 blocks per item... is this fesible?

# note: highest index seen so far 0x0429, but in theory
# could be as high as twice the number of items in base

base = []
address = 0x0010
while True:
    if (info[address] == 0x00 and info[address+1] == 0x00) or \
            (info[address] == 0xFF and info[address+1] == 0xFF):
        break
    else:
        base.append((info[address]) + (info[address+1] * 256))
        address += 2

sbase = set(base)
print("Base Section")
print("Count: ", len(base))
print("Unique values: ", len(list(sbase)))
print("Highest value: ", hex(max(sbase)))
print()

# overdub starts at 00000524.
overdub = []
address = 0x0524
for i in range(len(base)):
    overdub.append((info[address]) + (info[address+1] * 256))
    address += 2

#print(hexdump(info[address-32:address+32]))

soverdub = set(overdub)
print("Overdub Section")
print("Count: ", len(overdub))
print("Unique values: ", len(list(soverdub)))
print("Highest value: ", hex(max(soverdub)))
print("")

stotal = set (base + overdub)
print("Total")
print("Unique values: ", len(list(stotal)))
print("")


# Third section - it is not clear what this is for, probably doesn't
# hold enough information for a complete list. 

# Check TShark logs to confirm we download all of it...
'''
00000a30  00 00 00 00 00 00 00 00  6c 6f 6f 70 65 72 00 01  |........looper..|
00000a40  00 f7 fd ff b2 fe ff ba  fb ff 76 f6 ff 44 00 00  |..........v..D..|
00000a50  79 f7 ff 74 01 00 fb fd  ff cb 00 00 0f 00 00 8e  |y..t............|
...
00000bb0  ff ff b6 07 00 51 02 00  af ff ff e0 03 00 50 fe  |.....Q........P.|
00000bc0  ff af 04 00 74 fe ff d3  01 00 96 fb ff 9b fb ff  |....t...........|
00000bd0  c0 fb ff                                          |...|
00000bd3
'''

index = []
address = 0x0A3F        # through to 0x0bd3, 404 bytes

'''
for i in range(128):
    index.append((info[address]) + (info[address+1] * 256))
    address += 2
for i in range(128):
    index.append((info[address+2]) + (info[address+1] * 256) + \
            (info[address] * 256 * 256))
    address += 3
'''
for i in range(max([max(sbase), max(soverdub)])+1):
    index.append(i)

#print(hex(address))


# dump interpretted data
print("Base               : Overdub")
for i in range(len(base)):
    if base[i] == overdub[i] or overdub[i] == 0:
        print("%1.8f 0x%4.4X -> 0x%6.6X" % (i/len(base), base[i],  index[base[i]]))
    else:
        print("%1.8f 0x%4.4X -> 0x%6.6X : 0x%4.4X -> 0x%6.6X" % (i/len(base), \
                base[i], index[base[i]], overdub[i], index[overdub[i]]))

