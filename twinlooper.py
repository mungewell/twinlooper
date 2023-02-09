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

    def checksum(self, data):
        # 'Single Parity Check' algorythm
        check = 0x01
        for byte in data:
            check += int(byte)

        return bytes([(check & 0xFF) ^ 0xFF])

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

    def build_download(self, address, length):

        data = b""
        data += bytes([(address & 0xFF)])
        data += bytes([(address & 0xFF00) >> 8])
        data += bytes([(address & 0xFF0000) >> 16])
        data += bytes([(address & 0xFF000000) >> 24])

        data += bytes([(length & 0xFF)])
        data += bytes([(length & 0xFF00) >> 8])
        data += bytes([(length & 0xFF0000) >> 16])

        data += self.checksum(data)

        length = len(data)*8
        packed = self.pack(bytes(data), length)

        return(b"\x00\x32\x0d\x41\x00\x00\x40\x00" + packed)

#--------------------------------------------------
def main():
    from argparse import ArgumentParser
    from hexdump import hexdump
    from time import sleep

    parser = ArgumentParser(prog="zoomzt2")

    parser.add_argument("-d", "--debug",
        action="store_true", dest="debug",
        help="print out debug information")

    parser.add_argument("-s", "--skipsong",
        type=int, default=0, dest="skipsong",
        help="skip songs in info list, helpful if many")
    parser.add_argument("-b", "--base",
        action="store_true", dest="base",
        help="download the audio from the 'base'")
    parser.add_argument("-o", "--ovedub",
        action="store_true", dest="overdub",
        help="download the audio with the most recent 'overdub'")

    options = parser.parse_args()

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

    skipsong = options.skipsong
    found = False
    for address in range(0x1EF3E000, 0x1EF00000, -0x2000):
        print("Checking Song:", hex(address))

        mdata = pedal.build_download(address, 2)
        blen = (mdata[5]*128*128) + (mdata[4]*128) + mdata[3]
        
        if options.debug:
            print(hexdump(mdata))
            print(hexdump(pedal.unpack(mdata[8:],65)))

        msg = mido.Message("sysex", data = mdata)
        outport.send(msg); sleep(0); msg = inport.receive()

        blen = (msg.data[5]*128*128) + (msg.data[4]*128) + msg.data[3]
        rsp = pedal.unpack(bytes(msg.data)[8:], blen)
        if options.debug:
            print("Unpacked Response:")
            print(hexdump(rsp))

        # check if address contains data, assuming that's what these bytes mean
        #print(hex(rsp[7]), hex(rsp[8]))
        if (rsp[7] != 0xFF) or (rsp[8] != 0xFF):
            print("Song Found")
            if skipsong:
                skipsong -= 1
            else:
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

    outfile = open("info.bin", "wb")

    info = b""
    part = 0
    while length:
        # read 'info' block in 3 chunks
        print("Reading Info :", part)
        part += 1

        if length >= 0x03F1:
            mdata = pedal.build_download(address, 0x3F1)
            address += 0x03F1
            length -= 0x03F1
        else:
            mdata = pedal.build_download(address, length)
            length = 0

        if options.debug:
            print(hexdump(mdata))
            print(hexdump(pedal.unpack(mdata[8:],65)))

        msg = mido.Message("sysex", data = mdata)
        outport.send(msg); sleep(0); msg = inport.receive()

        blen = (msg.data[5]*128*128) + (msg.data[4]*128) + msg.data[3]
        rsp = pedal.unpack(bytes(msg.data)[8:], blen)

        if options.debug:
            print(hexdump(rsp[:64]))

        dlen = (rsp[6]*256*256) + (rsp[5]*256) + rsp[4]
        outfile.write(rsp[7:7 + dlen])
        info += rsp[7:7 + dlen]

    outfile.close()
    print("---")

    outfile = open("stream.raw", "wb")

    #print(hexdump(info[:64]))
    size = (info[13] * 256) + info[12]

    # we'll just try one index for now, should parse info to make a list
    index = 0x1234

    # just pull audio data from a hardcoded address.....
    group = 0x0127F000

    part = 0
    for address in range(group, group + (size * 0x1000), 0x1000):
        length = (0x03F1) * 4 + 0x38

        while length:
            # read 'audio' block in 5 chunks
            print("Download Audio : 0x%4.4x %d.%d - 0x%8.8x" % \
                    (index, part/5, part % 5, address))

            if length >= 0x03F1:
                mdata = pedal.build_download(address, 0x3F1)
                address += 0x03F1
                length -= 0x03F1
            else:
                mdata = pedal.build_download(address, length)
                length = 0
            part += 1

            if options.debug:
                print(hexdump(mdata))
                print(hexdump(pedal.unpack(mdata[8:],65)))

            msg = mido.Message("sysex", data = mdata)
            outport.send(msg); sleep(0); msg = inport.receive()

            blen = (msg.data[5]*128*128) + (msg.data[4]*128) + msg.data[3]
            audio = pedal.unpack(bytes(msg.data)[8:], blen)

            if options.debug:
                print("blen:", blen)
                print(hexdump(audio[:64]))

            # 'raw' audio can be converted with:
            # sox -r 48k -e signed -b 24 -c 2 --endian little stream.raw stream.wav

            dlen = (audio[6]*256*256) + (audio[5]*256) + audio[4]
            outfile.write(audio[7: 7 + dlen])


if __name__ == "__main__":
    main()

