'''
twinlooper.py (c) 2023-02-03 - Simon Wood (simon@mungewell.org)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

import mido

# may need to change for different pedals
midiname = "DFU"

class twinlooper(object):

    inport = None
    outport = None

    def is_connected(self):
        if self.inport == None or self.outport == None:
            return(False)
        else:
            return(True)

    def connect(self, midiskip = 0):
        if self.is_connected():
            return(True)

        skip = midiskip
        for port in mido.get_input_names():
            if port[:len(midiname)]==midiname:
                if not skip:
                    self.inport = mido.open_input(port)
                    break
                else:
                    skip = skip - 1

        skip = midiskip
        for port in mido.get_output_names():
            if port[:len(midiname)]==midiname:
                if not skip:
                    self.outport = mido.open_output(port)
                    break
                else:
                    skip = skip - 1

        if self.inport == None or self.outport == None:
            #print("Unable to find Pedal")
            return(False)
        return(True)

    def disconnect(self):
        self.inport = None
        self.outport = None

    #-----------------------------------

    def pack(self, input, bits=0):
        sum = 0
        offset = 0
        output = b""

        for data in input:
            sum += data << offset
            output += bytes([sum & 0x7F])
            bits -= 7
            sum = sum >> 7

            # accumulated enough bits for extra output
            if offset == 7:
                output += bytes([sum & 0x7F])
                bits -= 7
                sum = sum >> 7
                offset = 1
            else:
                offset += 1

        # output final byte
        if sum:
            output += bytes([sum & 0x7F])
            bits -= 7
        while bits >= 0:
            output += b"\x00"
            bits -= 7

        return(output)


    def unpack(self, input, bits=0):
        sum = 0
        offset = 0
        output = b""

        for data in input:
            sum += data << offset
            if offset == 0:
                offset = 7
                continue
            else:
                offset -= 1

            output += bytes([sum & 0xFF])
            sum = sum >> 8
            bits -= 8

        # output final byte
        if sum:
            output += bytes([sum & 0xFF])
            bits -= 8
        while bits >= 0:
            output += b"\x00"
            bits -= 8

        return(output)

    '''
    # test code for self.packing/unpacking
    from hexdump import hexdump
    data = self.pack(b"\x00\xFF\x00\xFF\x00\xFF\x00\xFF\x00", 72)
    print(hexdump(data))
    print(hexdump(unpack(data,72)))

    data = self.pack(b"\xFF\x00\xFF\x00\xFF\x00\xFF\x00\xFF", 72)
    print(hexdump(data))
    print(hexdump(unpack(data,72)))
    quit()
    '''

    def checksum(self, data, seed=0x00):
        # XOR checksum on self.unpacked data
        check = seed
        for byte in data:
            check ^= byte

        return bytes([check])

    def build_search(self, address):
        # f0:00:32:0d:41:00:00:40:00:00:20:62:7b:10:7e:00:00:73:01:f7

        data = bytearray(b"\x00\x00\xF8\xBC\x07\x01\x00\x00")
        data[2] = address & 0xFF
        data[3] = address >> 8

        if address < 0xBC80:
            data[7] = 0x80      # no idea why...

        data += self.checksum(data)
        length = len(data)*8
        packed = self.pack(bytes(data), length)

        # '0x41' is not enough bits for some messages, but following doesn't work...
        #mdata = b"\x00\x32\x0d" + bytes([length]) + b"\x00\x00\x40" + self.packed

        return(b"\x00\x32\x0d\x41\x00\x00\x40" + packed)

    def build_download(self, address):
        # f0:00:32:0d:41:00:00:40:00:00:20:62:7b:10:7e:00:00:73:01:f7

        data = bytearray(b"\x00\x00\x48\xBC\x87\xF8\x01\x00")
        #                                                   + XOR self.checksum
        #                                                ^^ ??
        #                                        ^^  ^^     size
        #                                    ^^ action/command
        #                            ^^  ^^ address / channel

        data[2] = address & 0xFF
        data[3] = address >> 8

        if address < 0xBC80:
            data[7] = 0x80      # no idea why...

        data += self.checksum(data, 0x73)
        length = len(data)*8
        packed = self.pack(bytes(data), length)

        return(b"\x00\x32\x0d\x41\x00\x00\x40" + packed)

    def build_ack(self, address):
        # f0:00:32:0d:41:00:00:40:00:62:2f:62:7b:60:4b:00:00:1e:01:f7

        '''
        # test to figure out what 'seed' to use
        test = b"\x00\x32\x0d\x41\x00\x00\x40\x00\x62\x2f\x62\x7b\x60\x4b\x00\x00\x1e\x01"
        print(hexdump(test))
        self.unpacked = self.unpack(test[7:])
        print(hexdump(unpacked))
        seed = self.checksum(unpacked)[0]
        print("checksum seed", hex(seed))

        print(hexdump(self.checksum(unpacked[0:-1], seed)))
        '''

        # so far only following address works...
        #address = 0xBC4B

        data = bytearray(b"\x00\xF1\x4B\xBC\x07\x2F\x01\x00")
        #                        ^^ ????

        data[2] = address & 0xFF
        data[3] = address >> 8

        data += self.checksum(data, 0x60)
        length = len(data)*8
        packed = self.pack(bytes(data), length)

        return(b"\x00\x32\x0d\x41\x00\x00\x40" + packed)

    #-----------------------------------
    # More Unpacked commands from logs
    downmr = b"\x00\x00\xFC\x30\x80\xF8\x01\x80"


#--------------------------------------------------
def main():
    from hexdump import hexdump
    from time import sleep

    pedal = twinlooper()
    if pedal.connect():
        inport = pedal.inport
        outport = pedal.outport
    else:
        print("Unable to locate pedal:", midiname)
        quit()

    print(pedal)

    # attempt to ID pedal
    msg = mido.Message("sysex", data = [0x00, 0x32, 0x45, 0x00, 0x00, 0x00, 0x40, 0x7f])
    outport.send(msg); sleep(0); msg = inport.receive()

    print("Found pedal:")
    print(hexdump(pedal.unpack(bytes(msg.data)[7:-1])))

    # do 'something'
    msg = mido.Message("sysex", data = [ \
            0x00, 0x32, 0x0d, 0x41, 0x00, 0x00, 0x00, 0x00, 0x00, \
            0x43, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x4e, 0x00 ])
    outport.send(msg); sleep(0); msg = inport.receive()

    print("'something'")
    print("Unpacked Response:")
    blen = (msg.data[5]*128*128) + (msg.data[4]*128) + msg.data[3]
    print(hexdump(pedal.unpack(bytes(msg.data)[7:-1], blen)))

    # search for 'address' of data to download
    print("---")

    for address in range(0xBCF8, 0xBC00, -8):
        print("Checking Address:", hex(address))
        msg = mido.Message("sysex", data = pedal.build_search(address))
        outport.send(msg); sleep(0); msg = inport.receive()

        print("Unpacked Response:")
        blen = (msg.data[5]*128*128) + (msg.data[4]*128) + msg.data[3]
        rsp = pedal.unpack(bytes(msg.data)[7:-1], blen)
        print(hexdump(rsp))

        '''
        # test to perform/force more 'searches'
        if address > 0xBC78:
            continue
        '''
        
        # check if address contains data, assuming that's what these bytes mean
        #print(hex(rsp[7]), hex(rsp[8]))
        if (rsp[7] != 0xFF) or (rsp[8] & 0x7F != 0x7F):
            break

        sleep(0)

    # attempt to download at current address.
    print("---")

    print("Download Address (pt1):", hex(address))
    msg = mido.Message("sysex", data = pedal.build_download(address))
    outport.send(msg); sleep(0); msg = inport.receive()

    print("Unpacked Response (crop):")
    blen = (msg.data[5]*128*128) + (msg.data[4]*128) + msg.data[3]
    pt1 = pedal.unpack(bytes(msg.data)[7:-1], blen)
    print(hexdump(pt1[:64]))

    # try 'part 2'
    print("Download Address (pt 2):", hex(address))
    msg = mido.Message("sysex", data = pedal.build_download(address+1))
    outport.send(msg); sleep(0); msg = inport.receive()

    print("Unpacked Response (crop):")
    blen = (msg.data[5]*128*128) + (msg.data[4]*128) + msg.data[3]
    pt2 = pedal.unpack(bytes(msg.data)[7:-1], blen)
    print(hexdump(pt2[:64]))

    # and do 'ack'
    print("Ack Address:", hex(address))
    msg = mido.Message("sysex", data = pedal.build_ack(address+4))
    outport.send(msg); sleep(0); msg = inport.receive()

    print("Unpacked Response (crop):")
    blen = (msg.data[5]*128*128) + (msg.data[4]*128) + msg.data[3]
    ack = pedal.unpack(bytes(msg.data)[7:-1], blen)
    print(hexdump(ack[:64]))

if __name__ == "__main__":
    main()

