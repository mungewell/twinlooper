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

    def reverse_check(self, data):
        from hexdump import hexdump

        print(hexdump(data))
        for i in range(len(data)):
            unpacked = self.unpack(data[i:])
            print(hexdump(unpacked))
            seed = self.checksum(unpacked)[0]
            print("checksum seed", i, hex(seed))

    def build_something(self):
        # host    1.3.2   f0:00:32:0d:41:00:00:00:00:00:43:00:00:00:02:00:00:4e:00:f7
        # 00000000: 80 21 00 00 10 00 00 4E                           .!.....N
        # 1.3.1   host    f0:00:32:0d:41:01:00:00:00:00:43:00:00:00:02:00:00:01:00:00
        #                :00:50:62:09:00:00:20:54:15:08:16:03:23:58:72:5e:05:f7
        # 00000000: 80 21 00 00 10 00 00 01  00 00 00 15 27 00 00 10  .!..........'...
        # 00000010: B5 82 B0 0C 46 58 B9 B7                           ....FX..
        # checksum seed 8 0x9
        print()


    def build_search(self, address):
        # host    1.3.2   f0:00:32:0d:41:00:00:40:00:00:60:67:7b:20:00:00:00:04:01:f7
        # ...
        # host    1.3.2   f0:00:32:0d:41:00:00:40:00:00:40:62:7b:20:00:00:00:55:01:f7
        # 00000000: 00 A0 78 0F 02 00 00 D5                           ..x.....
        # 1.3.1   host    f0:00:32:0d:51:00:00:40:00:00:40:62:7b:20:00:00:00:7f:7f:5f:06:f7 
        # 00000000: 00 A0 78 0F 02 00 00 FF  FF D7                    ..x.......
        # host    1.3.2   f0:00:32:0d:41:00:00:40:00:00:20:62:7b:20:00:00:00:65:01:f7
        # 00000000: 00 90 78 0F 02 00 00 E5                           ..x.....
        # 1.3.1   host    f0:00:32:0d:51:00:00:40:00:00:20:62:7b:20:00:00:00:6c:5e:29:00:f7
        # 00000000: 00 90 78 0F 02 00 00 6C  6F 0A                    ..x....lo.  -> found!

        data = bytearray(b"\x00\xF0\x79\x0F\x02\x00\x00")
        data[1] = address & 0xFF
        data[2] = address >> 8

        data += self.checksum(data, 0x00)
        length = len(data)*8
        packed = self.pack(bytes(data), length)

        return(b"\x00\x32\x0d\x41\x00\x00\x40\x00" + packed)

    def build_download1(self, address):
        # host    1.3.2   f0:00:32:0d:41:00:00:40:00:00:20:62:7b:10:7e:00:00:73:01:f7
        # 00000000: 00 90 78 0F F1 03 00 F3                           ..x.....

        data = bytearray(b"\x00\x90\x78\x0F\xF1\x03\x00")
        #                                                + XOR self.checksum
        #                                            ^^ ??
        #                                    ^^  ^^     size
        #                                ^^ action/command
        #                        ^^  ^^ address / channel

        data[1] = address & 0xFF
        data[2] = address >> 8

        data += self.checksum(data, 0xE6)
        length = len(data)*8
        packed = self.pack(bytes(data), length)

        return(b"\x00\x32\x0d\x41\x00\x00\x40\x00" + packed)

    def build_download2(self, address):
        # host    1.3.2   f0:00:32:0d:41:00:00:40:00:71:27:62:7b:10:7e:00:00:7f:01:f7
        # 00000000: F1 93 78 0F F1 03 00 FF                           ..x.....

        data = bytearray(b"\xF1\x90\x78\x0F\xF1\x03\x00")
        #                                                + XOR self.checksum
        #                                            ^^ ??
        #                                    ^^  ^^     size
        #                                ^^ action/command
        #                        ^^  ^^ address / channel

        data[1] = address & 0xFF
        data[2] = address >> 8

        data += self.checksum(data, 0x18)
        length = len(data)*8
        packed = self.pack(bytes(data), length)

        return(b"\x00\x32\x0d\x41\x00\x00\x40\x00" + packed)

    def build_ack(self, address):
        # f0:00:32:0d:41:00:00:40:00:62:2f:62:7b:60:4b:00:00:1e:01:f7
        # 00000000: E2 97 78 0F 5E 02 00 9E                           ..x.^...

        # host    1.3.2   f0:00:32:0d:41:00:00:40:00:62:7f:07:03:40:03:00:00:20:01:f7
        # 00000000: E2 FF 61 00 1C 00 00 A0                           ..a.....
        # checksum seed 8 0xc0
        # host    1.3.2   f0:00:32:0d:41:00:00:40:00:62:0f:00:03:40:03:00:00:19:01:f7
        # 00000000: E2 07 60 00 1C 00 00 99                           ..`.....
        # checksum seed 8 0x0
        # host    1.3.2   f0:00:32:0d:41:00:00:40:00:62:1f:00:03:40:03:00:00:11:01:f7
        # 00000000: E2 0F 60 00 1C 00 00 91                           ..`.....
        # checksum seed 8 0x0

        data = bytearray(b"\xE2\x97\x78\x0F\x5E\x02\x00")

        data[1] = address & 0xFF
        data[2] = address >> 8

        data += self.checksum(data, 0xC0)
        length = len(data)*8
        packed = self.pack(bytes(data), length)

        return(b"\x00\x32\x0d\x41\x00\x00\x40\00" + packed)

    def build_more1(self):
        # host    1.3.2   f0:00:32:0d:41:00:00:40:00:00:70:07:03:10:7e:00:00:31:01:f7
        # 00000000: 00 F8 61 00 F1 03 00 B1                           ..a.....
        # checksum seed 8 0xda
        # host    1.3.2   f0:00:32:0d:41:00:00:40:00:71:77:07:03:10:7e:00:00:3d:01:f7
        # 00000000: F1 FB 61 00 F1 03 00 BD                           ..a.....
        # checksum seed 8 0x24

        data = bytearray(b"\x00\xF8\x61\x00\xF1\x03\x00")

        data += self.checksum(data, 0xDA)
        length = len(data)*8
        packed = self.pack(bytes(data), length)

        return(b"\x00\x32\x0d\x41\x00\x00\x40\00" + packed)

    def build_more2(self):
        # host    1.3.2   f0:00:32:0d:41:00:00:40:00:00:70:07:03:10:7e:00:00:31:01:f7
        # 00000000: 00 F8 61 00 F1 03 00 B1                           ..a.....
        # checksum seed 8 0xda
        # host    1.3.2   f0:00:32:0d:41:00:00:40:00:71:77:07:03:10:7e:00:00:3d:01:f7
        # 00000000: F1 FB 61 00 F1 03 00 BD                           ..a.....
        # checksum seed 8 0x24

        data = bytearray(b"\xF1\xFB\x61\x00\xF1\x03\x00")

        data += self.checksum(data, 0x24)
        length = len(data)*8
        packed = self.pack(bytes(data), length)

        return(b"\x00\x32\x0d\x41\x00\x00\x40\00" + packed)

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

    # attempt to ID pedal
    msg = mido.Message("sysex", data = [0x00, 0x32, 0x45, 0x00, 0x00, 0x00, 0x40, 0x7f])
    outport.send(msg); sleep(0); msg = inport.receive()

    print("Found pedal:")
    print(hexdump(pedal.unpack(bytes(msg.data)[8:-1])))

    # do 'something'
    msg = mido.Message("sysex", data = [ \
            0x00, 0x32, 0x0d, 0x41, 0x00, 0x00, 0x00, 0x00, 0x00, \
            0x43, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x4e, 0x00 ])
    outport.send(msg); sleep(0); msg = inport.receive()

    print("'something'")
    print("Unpacked Response:")
    blen = (msg.data[5]*128*128) + (msg.data[4]*128) + msg.data[3]
    print(hexdump(pedal.unpack(bytes(msg.data)[8:-1], blen)))

    # search for 'address' of data to download
    print("---")

    for address in range(0x79F0, 0x7800, -16):
        print("Checking Address:", hex(address))
        msg = mido.Message("sysex", data = pedal.build_search(address))
        outport.send(msg); sleep(0); msg = inport.receive()

        print("Unpacked Response:")
        blen = (msg.data[5]*128*128) + (msg.data[4]*128) + msg.data[3]
        rsp = pedal.unpack(bytes(msg.data)[8:-1], blen)
        print(hexdump(rsp))

        '''
        # test to perform/force more 'searches'
        if address > 0xBC78:
            continue
        
        # check if address contains data, assuming that's what these bytes mean
        #print(hex(rsp[7]), hex(rsp[8]))
        if (rsp[7] != 0xFF) or (rsp[8] != 0xFF):
            break
        '''

        sleep(0)

    # attempt to download at current address.
    print("---")

    print("Download Address (pt1):", hex(address))
    msg = mido.Message("sysex", data = pedal.build_download1(address))
    outport.send(msg); sleep(0); msg = inport.receive()

    print("Unpacked Response (crop):")
    blen = (msg.data[5]*128*128) + (msg.data[4]*128) + msg.data[3]
    pt1 = pedal.unpack(bytes(msg.data)[8:-1], blen)
    print(hexdump(pt1[:64]))

    # try 'part 2'
    print("Download Address (pt 2):", hex(address))
    msg = mido.Message("sysex", data = pedal.build_download2(address+3))
    outport.send(msg); sleep(0); msg = inport.receive()

    print("Unpacked Response (crop):")
    blen = (msg.data[5]*128*128) + (msg.data[4]*128) + msg.data[3]
    pt2 = pedal.unpack(bytes(msg.data)[8:-1], blen)
    print(hexdump(pt2[:64]))

    outfile = open("stream.raw", "wb")
    for i in range(10):
        # and do 'ack'
        print("ack address:", hex(address))
        msg = mido.Message("sysex", data = pedal.build_ack(address+7))
        outport.send(msg); sleep(0); msg = inport.receive()

        print("unpacked response (crop):")
        blen = (msg.data[5]*128*128) + (msg.data[4]*128) + msg.data[3]
        ack = pedal.unpack(bytes(msg.data)[8:-1], blen)
        print(hexdump(ack[:64]))

        # now do 'more'
        print("more1:")
        msg = mido.Message("sysex", data = pedal.build_more1())
        outport.send(msg); sleep(0); msg = inport.receive()

        print("unpacked response (crop):")
        blen = (msg.data[5]*128*128) + (msg.data[4]*128) + msg.data[3]
        more1 = pedal.unpack(bytes(msg.data)[8:-1], blen)
        print(hexdump(more1[:64]))

        # sox -r 48k -e signed -b 24 -c 2 --endian big stream.raw stream.wav
        outfile.write(more1[7:])

        # now do 'more'
        print("more2:")
        msg = mido.Message("sysex", data = pedal.build_more2())
        outport.send(msg); sleep(0); msg = inport.receive()

        print("unpacked response (crop):")
        blen = (msg.data[5]*128*128) + (msg.data[4]*128) + msg.data[3]
        more2 = pedal.unpack(bytes(msg.data)[8:-1], blen)
        print(hexdump(more2[:64]))

        #outfile.write(more2[7:])

    #pedal.reverse_check(b"\x00\x32\x0d\x41\x00\x00\x40\x00\x00\x70\x07\x03\x10\x7e\x00\x00\x31\x01")
    #pedal.reverse_check(b"\x00\x32\x0d\x41\x00\x00\x40\x00\x71\x77\x07\x03\x10\x7e\x00\x00\x3d\x01")

if __name__ == "__main__":
    main()

