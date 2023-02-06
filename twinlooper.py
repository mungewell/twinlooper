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

        while check & 0xFFFF00:
            check2 = (check & 0xFF) + (check >> 8)
            check =check2

        return bytes([check ^ 0xFF])

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

    def build_download(self, address, length, seed=0x00):

        data = b""
        data += bytes([(address & 0xFF)])
        data += bytes([(address & 0xFF00) >> 8])
        data += bytes([(address & 0xFF0000) >> 16])
        data += bytes([(address & 0xFF000000) >> 24])

        data += bytes([(length & 0xFF)])
        data += bytes([(length & 0xFF00) >> 8])
        data += bytes([(length & 0xFF0000) >> 16])

        data += self.checksum(data, seed)

        length = len(data)*8
        packed = self.pack(bytes(data), length)

        return(b"\x00\x32\x0d\x41\x00\x00\x40\x00" + packed)

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

    print("Located pedal:")
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
    for address in range(0x1EF3E000, 0x1EF00000, -0x2000):
        print("Checking Address:", hex(address))

        mdata = pedal.build_download(address, 2)
        blen = (mdata[5]*128*128) + (mdata[4]*128) + mdata[3]
        
        #print(hexdump(mdata))
        #print(hexdump(pedal.unpack(mdata[8:],65)))

        msg = mido.Message("sysex", data = mdata)
        outport.send(msg); sleep(0); msg = inport.receive()

        print("Unpacked Response:")
        blen = (msg.data[5]*128*128) + (msg.data[4]*128) + msg.data[3]
        rsp = pedal.unpack(bytes(msg.data)[8:], blen)
        print(hexdump(rsp))

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

    # from Tshark logs...
    length = 0x03F1 + 0x03F1 + 0x025E
    index = 0
    seed = [0xFE, 0xFD, 0xFD]

    outfile = open("info.bin", "wb")
    while length:
        # read 'info' block in 3 chunks
        if length >= 0x03F1:
            mdata = pedal.build_download(address, 0x3F1, seed[index])
            address += 0x03F1
            length -= 0x03F1
        else:
            mdata = pedal.build_download(address, length, seed[index])
            length = 0

        print(hexdump(mdata))
        print(hexdump(pedal.unpack(mdata[8:],65)))

        msg = mido.Message("sysex", data = mdata)
        outport.send(msg); sleep(0); msg = inport.receive()

        print("Info - Unpacked Response (crop):", index)
        blen = (msg.data[5]*128*128) + (msg.data[4]*128) + msg.data[3]
        info = pedal.unpack(bytes(msg.data)[8:], blen)
        print(hexdump(info[:64]))

        dlen = (info[6]*256*256) + (info[5]*256) + info[4]
        outfile.write(info[7:7 + dlen])
        index += 1

    outfile.close()

    print("---")

    # just pull audio data from a hardcoded address..... some examples.
    # should really parse the info data to find out what to download
    address = 0x0127F000
    seed = [0xFE, 0xFD, 0xFE, 0xFE, 0xFE]

    address = 0x000FF000
    seed = [0xFF, 0xFE, 0xFE, 0xFE, 0xFE]

    address = 0x000C0000
    seed = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

    length = (0x03F1) * 4 + 0x38
    index = 0

    outfile = open("stream.raw", "wb")
    while length:
        # read 'audio' block in 5 chunks
        if length >= 0x03F1:
            mdata = pedal.build_download(address, 0x3F1, seed[index])
            address += 0x03F1
            length -= 0x03F1
        else:
            mdata = pedal.build_download(address, length, seed[index])
            length = 0

        print(hexdump(mdata))
        print(hexdump(pedal.unpack(mdata[8:],65)))

        msg = mido.Message("sysex", data = mdata)
        outport.send(msg); sleep(0); msg = inport.receive()

        print("Audio - Unpacked Response (crop):", index)
        blen = (msg.data[5]*128*128) + (msg.data[4]*128) + msg.data[3]
        audio = pedal.unpack(bytes(msg.data)[8:], blen)
        #print("blen:", blen)
        print(hexdump(audio[:64]))

        # 'raw' audio can be converte with:
        # sox -r 48k -e signed -b 24 -c 2 --endian big stream.raw stream.wav

        dlen = (audio[6]*256*256) + (audio[5]*256) + audio[4]
        #print("len:", len(audio))
        #print("dlen:", dlen)

        outfile.write(audio[7:-2])
        index += 1


if __name__ == "__main__":
    main()

