
Log download using official tool, however this failed to render the 'song.wav' file.

First audio block was
    # 00 F0 83 11 = 0x1183F000

Then 2nd was
    # 00 00 80 11 = 0x11800000


The 2nd matches the whole memory (download from same address) and LTC-dumps as the start of the 'song'
--
$ sox -r 48k -e signed -b 24 -c 2 --endian little 0x11800000.raw 0x11800000.wav

$ ~/ltc-tools-github/ltcdump -a -c 2 0x11800000.wav 
Note: This is not a mono audio file - using channel 2
0.040000	0.080000	No LTC frame found
0.077458	0.116500	00:00:00:00
0.116521	0.155562	00:00:00:01
0.155583	0.194625	00:00:00:02
0.194646	0.233687	00:00:00:03
0.233708	0.272750	00:00:00:04
0.272771	0.311812	00:00:00:05
0.311833	0.350875	00:00:00:06
0.350896	0.389937	00:00:00:07
0.389958	0.429000	00:00:00:08
--

So it seems that the first block is rendered after the base loop is recorded, and includes the fade in, which we saw in other logs.
