# twinlooper
Python code to interact with Rowin Twin Looper effects pedal

This project started as a discussion on the `loopertrx` project, which supports other pedals.
https://github.com/reinerh/loopertrx

It quickly transpired that my TwinLooper pedal (and others) did not support the same (USB Mass Storage) protocols, instead using Midi SysEx to communicate. From a WireShark log I was able to identify some aspects of this and have started this project.

At this time it should be considered _Experiemental_, there is a high chance that it could do something bad to your pedal (though mine seems OK so far).

Example:
The script connects to the pedal, attempts to 'search' for a recording and 'download' it (well the first 2 parts).
```
$ python3 twinlooper.py 
Found pedal:
00000000: 30 B1 31 B2 32 B3 33 B4  30 B1 31 B2 32 B3 33 B4  0.1.2.3.0.1.2.3.
00000010: 00 80 02 89 09 8A 0A 8B  0B 8C 8C                 ...........
None
'something'
Unpacked Response:
00000000: 00 C0 10 00 00 08 00 80  00 00 00 00 8B 13 00 80  ................
00000010: 05 94 6F 7C 72 8B 6F FC  0A                       ..o|r.o..
None
---
Checking Address: 0xbcf8
Unpacked Response:
00000000: 00 00 F8 BC 07 01 00 00  07 00 0B                 ...........
None
---
Download Address (pt1): 0xbcf8
Unpacked Response (crop):
00000000: 00 00 F8 BC 87 F8 01 00  07 00 80 0F 00 80 1F 00  ................
00000010: 00 2B 00 00 BA FF FF 56  00 00 A5 FF 7F 70 00 00  .+.....V.....p..
00000020: E9 FF FF B7 FF FF E0 FF  FF 0B 00 00 22 00 80 29  ............"..)
00000030: 00 80 F0 FF FF B5 FF FF  2B 00 80 25 00 00 86 00  ........+..%....
None
Download Address (pt 2): 0xbcf8
Unpacked Response (crop):
00000000: 00 00 F9 BC 87 F8 01 00  80 BC FF 7F AD FF FF 34  ...............4
00000010: 00 80 1E 00 00 EA FF FF  D4 FF FF 1C 00 80 10 00  ................
00000020: 80 D1 FF FF 24 00 00 D0  FF 7F F6 FF 7F 88 FF FF  ....$...........
00000030: FA FF 7F C5 FF FF 15 00  80 1A 00 80 DD FF FF 30  ...............0
None
Ack Address: 0xbcf8
```

At present the 'ACK' stalls, unless the specific address mentioned in the forementioned logs is used.... working on that. ;-)
