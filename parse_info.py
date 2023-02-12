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
        #base.append((info[address+1]) + (info[address] * 256))
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
    #overdub.append((info[address+1]) + (info[address] * 256))
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


# dump interpretted data
print("Base               : Overdub")
for i in range(len(base)):
    if base[i] == overdub[i] or overdub[i] == 0:
        print("%1.8f 0x%4.4X -> 0x%8.8X" % (i/(len(base)+1), base[i], base[i]))
        #print("%1.8f 0x%4.4X -> 0x%8.8X" % (i/(len(base)+1), base[i],  \
        #        ((base[i] >> 3 ) * 0x1000) + 0x086C0000))
    else:
        print("%1.8f 0x%4.4X -> 0x%4.4X : 0x%4.4X -> 0x%4.4X" % (i/(len(base)+1), \
                base[i], base[i], overdub[i], overdub[i]))

