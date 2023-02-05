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
        # 'Single Parity Check' algorythm
        check = seed
        for byte in data:
            check += int(byte)

        check2 = (check & 0xFF) + (check >> 8)

        return bytes([check2 ^ 0xFF])

    def reverse_check(self, data, min=1, max=9):
        from hexdump import hexdump

        print("Reverse")
        print(hexdump(data))
        for i in range(min, max):
            unpacked = self.unpack(data[i:])
            print(hexdump(unpacked))
            seed = self.checksum(unpacked)[0]
            print("checksum seed", i, hex(seed))

    def build_ident(self):
        # host    1.3.2   f0:00:32:45:00:00:00:40:7f:f7
        # 1.3.1   host    f0:00:32:45:58:01:00:40:30:62:46:11:2b:66:6c:19:34:61:44:0d
        #                :23:56:4c:59:33:68:02:00:28:20:62:04:0a:15:2c:5c:40:11:23:01:f7
        #
        # 00000000: 62 63 64 65 66 67 68 61  62 63 64 65 66 67 68 01  bcdefghabcdefgh.
        # 00000010: 00 05 12 13 14 15 16 17  18 19 05                 ...........
        print()

    def build_something(self):
        # host    1.3.2   f0:00:32:0d:41:00:00:00:00:00:43:00:00:00:02:00:00:4e:00:f7
        # 00000000: 80 21 00 00 10 00 00 4E                           .!.....N
        #
        # 1.3.1   host    f0:00:32:0d:41:01:00:00:00:00:43:00:00:00:02:00:00:01:00:00
        #                :00:50:62:09:00:00:20:54:15:08:16:03:23:58:72:5e:05:f7
        #
        # 00000000: 80 21 00 00 10 00 00 01  00 00 00 15 27 00 00 10  .!..........'...
        # 00000010: B5 82 B0 0C 46 58 B9 B7                           ....FX..
        # checksum seed 8 0x9

        # 0000 0001 0101 0010 0111 0000 = 0 15 27 0
        # 0000 0001 0000 1011 0101 1000 0000 = 0 10 B5 82 B0
        # 0000 1010 0100 0110 0101 1000 = 0C 46 58
        # 1011 1001 1011 0111 = B9 B7
        # 
        print()

    def build_download(self, packet, address, seed=0x00):

        data = bytearray(packet)
        data[1] = (address & 0xFF)
        data[2] = (address & 0xFF00) >> 8
        data[3] = (address & 0xFF0000) >> 16

        data += self.checksum(data, seed)

        length = len(data)*8
        packed = self.pack(bytes(data), length)

        return(b"\x00\x32\x0d\x41\x00\x00\x40\x00" + packed)

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

        return self.build_download(b"\x00\xF0\x79\x0F\x02\x00\x00", address)

    def build_info1(self, address):
        # host    1.3.2   f0:00:32:0d:41:00:00:40:00:00:20:62:7b:10:7e:00:00:73:01:f7
        # 00000000: 00 90 78 0F F1 03 00 F3                           ..x.....

        return self.build_download(b"\x00\x80\xF0\x1F\xF1\x03\x00", address, 0xFE)

    def build_info2(self, address):
        # host    1.3.2   f0:00:32:0d:41:00:00:40:00:71:27:62:7b:10:7e:00:00:7f:01:f7
        # 00000000: F1 93 78 0F F1 03 00 FF                           ..x.....

        return self.build_download(b"\xF1\x80\xF0\x1F\xF1\x03\x00", address, 0xFD)

    def build_info3(self, address):
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

        return self.build_download(b"\xE2\x80\xF0\x1F\xF1\x03\x00", address, 0xFD)

    def build_more1(self, address):
        # host    1.3.2   f0:00:32:0d:41:00:00:40:00:00:70:07:03:10:7e:00:00:31:01:f7
        # 00000000: 00 F8 61 00 F1 03 00 B1                           ..a.....
        # checksum seed 8 0xda
        # host    1.3.2   f0:00:32:0d:41:00:00:40:00:71:77:07:03:10:7e:00:00:3d:01:f7
        # 00000000: F1 FB 61 00 F1 03 00 BD                           ..a.....
        # checksum seed 8 0x24

        return self.build_download(b"\x00\x80\xF0\x1F\xF1\x03\x00", address)

    def build_more2(self, address):
        # host    1.3.2   f0:00:32:0d:41:00:00:40:00:00:70:07:03:10:7e:00:00:31:01:f7
        # 00000000: 00 F8 61 00 F1 03 00 B1                           ..a.....
        # checksum seed 8 0xda
        # host    1.3.2   f0:00:32:0d:41:00:00:40:00:71:77:07:03:10:7e:00:00:3d:01:f7
        # 00000000: F1 FB 61 00 F1 03 00 BD                           ..a.....
        # checksum seed 8 0x24

        return self.build_download(b"\xF1\x80\xF0\x1F\xF1\x03\x00", address, 0xFE)


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
    #print(hexdump(pedal.unpack(bytes(msg.data)[8:-1])))
    blen = (msg.data[5]*128*128) + (msg.data[4]*128) + msg.data[3]
    ident = pedal.unpack(msg.data, blen)

    print(hexdump(ident))
    '''
    dlen = (ident[5]*256*256) + (ident[4]*256) + ident[3]
    print(hexdump(ident[6:6 + dlen]))
    '''

    # do 'something'
    msg = mido.Message("sysex", data = [ \
            0x00, 0x32, 0x0d, 0x41, 0x00, 0x00, 0x00, 0x00, 0x00, \
            0x43, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x4e, 0x00 ])
    outport.send(msg); sleep(0); msg = inport.receive()

    print("'something'")
    print("Unpacked Response:")
    blen = (msg.data[5]*128*128) + (msg.data[4]*128) + msg.data[3]
    something = pedal.unpack(msg.data, blen)

    print(hexdump(something))
    '''
    dlen = (ident[5]*256*256) + (ident[4]*256) + ident[3]
    print(hexdump(something[6:6 + dlen]))
    '''

    # search for 'address' of data to download
    print("---")

    found = False
    for address in range(0x1EF3E0, 0x1EF000, -32):
        print("Checking Address:", hex(address))

        mdata = pedal.build_search(address)
        print(mdata)
        print(hexdump(mdata))

        blen = (mdata[5]*128*128) + (mdata[4]*128) + mdata[3]
        
        '''
        print(hexdump(mdata))
        print(hexdump(pedal.unpack(mdata[8:],65)))
        '''
        msg = mido.Message("sysex", data = pedal.build_search(address))
        outport.send(msg); sleep(0); msg = inport.receive()

        print("Unpacked Response:")
        blen = (msg.data[5]*128*128) + (msg.data[4]*128) + msg.data[3]
        rsp = pedal.unpack(bytes(msg.data)[8:], blen)
        print(hexdump(rsp))

        '''
        # test to perform/force more 'searches'
        if address > 0xF200:
            continue
        '''
        
        # check if address contains data, assuming that's what these bytes mean
        #print(hex(rsp[7]), hex(rsp[8]))
        if (rsp[7] != 0xFF) or (rsp[8] != 0xFF):
            found = True
            break

        sleep(0)

    if not found:
        print("Unable to locate 'song'")
        quit()

    # attempt to download 'info' at current address.
    print("---")
    outfile = open("info.bin", "wb")

    msg = mido.Message("sysex", data = pedal.build_info1(address))
    outport.send(msg); sleep(0); msg = inport.receive()

    print("Unpacked Response (crop):")
    blen = (msg.data[5]*128*128) + (msg.data[4]*128) + msg.data[3]
    info1 = pedal.unpack(bytes(msg.data)[8:], blen)
    print(hexdump(info1[:64]))

    dlen = (info1[6]*256*256) + (info1[5]*256) + info1[4]
    outfile.write(info1[7:7 + dlen])

    # do 'part 2'
    print("Info (pt 2):", hex(address))
    print(hexdump(pedal.build_info2(address)))

    msg = mido.Message("sysex", data = pedal.build_info2(address+3))
    outport.send(msg); sleep(0); msg = inport.receive()

    print("Unpacked Response (crop):")
    blen = (msg.data[5]*128*128) + (msg.data[4]*128) + msg.data[3]
    info2 = pedal.unpack(bytes(msg.data)[8:], blen)
    print(hexdump(info2[:64]))

    dlen = (info2[6]*256*256) + (info2[5]*256) + info2[4]
    outfile.write(info2[7:7 + dlen])

    # and do 'part-3'
    print("Info (pt3):", hex(address))
    msg = mido.Message("sysex", data = pedal.build_info3(address+7))
    outport.send(msg); sleep(0); msg = inport.receive()

    print("unpacked response (crop):")
    blen = (msg.data[5]*128*128) + (msg.data[4]*128) + msg.data[3]
    info3 = pedal.unpack(bytes(msg.data)[8:], blen)
    print(hexdump(info3[:64]))

    dlen = (info3[6]*256*256) + (info3[5]*256) + info3[4]
    outfile.write(info3[7:7 + dlen])

    outfile.close()
    outfile = open("stream.raw", "wb")

    # just pull audio data from a hardcoded address.....
    # should really parse the info data to find out what to download

    for address in range(0x000FF0, 0x000FF8, 8):
        # now do 'more'
        print("more1:", address)
        msg = mido.Message("sysex", data = pedal.build_more1(address))
        outport.send(msg); sleep(0); msg = inport.receive()

        print("unpacked response (crop):")
        blen = (msg.data[5]*128*128) + (msg.data[4]*128) + msg.data[3]
        more1 = pedal.unpack(bytes(msg.data)[8:], blen)
        print(hexdump(more1[:64]))

        # sox -r 48k -e signed -b 24 -c 2 --endian big stream.raw stream.wav
        dlen = (msg.data[4]*256*256) + (msg.data[5]*256) + msg.data[6]
        outfile.write(more1[7:7 + dlen])

        # now do 'more'
        print("more2:")
        msg = mido.Message("sysex", data = pedal.build_more2(address+3))
        outport.send(msg); sleep(0); msg = inport.receive()

        print("unpacked response (crop):")
        blen = (msg.data[5]*128*128) + (msg.data[4]*128) + msg.data[3]
        more2 = pedal.unpack(bytes(msg.data)[8:], blen)
        print(hexdump(more2[:64]))

        outfile.write(more2[9:7 + dlen])

        # and do 'ack'
        '''
        print("ack address:", hex(address))
        msg = mido.Message("sysex", data = pedal.build_ack(address+7))
        outport.send(msg); sleep(0); msg = inport.receive()

        print("unpacked response (crop):")
        blen = (msg.data[5]*128*128) + (msg.data[4]*128) + msg.data[3]
        ack = pedal.unpack(bytes(msg.data)[8:], blen)
        print(hexdump(ack[:64]))
        '''

if __name__ == "__main__":
    main()

