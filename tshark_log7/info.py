import twinlooper
from hexdump import hexdump

infos = [b"\x00\x32\x0d\x49\x3f\x00\x40\x00\x00\x00\x4b\x77\x11\x7e\x00\x00\x6c\x5e\x3d\x03\x57\x4c\x1c\x00\x7f\x05\x00\x30\x05\x00\x22\x01\x01\x06\x00\x23\x10\x0c\x01\x31\x04\x46\x11\x20\x46\x20\x19\x02\x66\x08\x1c\x23\x00\x0d\x41\x34\x04\x54\x11\x58\x46\x20\x3a\x03\x6a\x0d\x2c\x37\x40\x5d\x41\x76\x06\x5c\x1b\x78\x6e\x00\x3c\x03\x71\x0d\x48\x37\x30\x5e\x01\x7a\x06\x6a\x1b\x30\x6f\x60\x3d\x03\x78\x0d\x64\x37\x20\x5f\x41\x7d\x06\x78\x1b\x68\x6f\x40\x3f\x03\x7f\x0d\x00\x38\x10\x60\x01\x01\x07\x06\x1c\x20\x70\x20\x41\x03\x06\x0e\x1c\x38\x00\x61\x41\x04\x07\x14\x1c\x70\x48\x60\x23\x02\x10\x09\x44\x24\x20\x12\x41\x49\x04\x28\x12\x28\x49\x40\x25\x02\x17\x09\x60\x24\x10\x13\x01\x4d\x04\x36\x12\x60\x49\x20\x27\x02\x1e\x09\x7c\x24\x00\x14\x41\x50\x04\x44\x12\x18\x4a\x00\x29\x02\x25\x09\x18\x25\x70\x14\x01\x54\x04\x52\x12\x50\x4a\x60\x2a\x02\x2c\x09\x34\x25\x60\x15\x41\x57\x04\x60\x12\x58\x70\x20\x43\x03\x0e\x0e\x3c\x38\x00\x62\x41\x08\x07\x24\x1c\x18\x71\x00\x45\x03\x15\x0e\x58\x38\x70\x62\x01\x0c\x07\x32\x1c\x50\x71\x60\x46\x03\x1c\x0e\x74\x38\x60\x63\x41\x0f\x07\x40\x1c\x08\x72\x40\x48\x03\x23\x0e\x10\x39\x50\x64\x01\x13\x07\x4e\x1c\x40\x72\x20\x4a\x03\x2a\x0e\x2c\x39\x40\x65\x01\x69\x04\x26\x13\x20\x4d\x20\x35\x02\x56\x09\x5c\x26\x00\x1b\x41\x6c\x04\x34\x13\x58\x4d\x00\x37\x02\x5d\x09\x78\x26\x70\x1b\x01\x70\x04\x42\x13\x10\x4e\x60\x38\x02\x64\x09\x14\x27\x60\x1c\x41\x73\x04\x50\x13\x48\x4e\x40\x3a\x02\x6b\x09\x30\x27\x50\x1d\x01\x77\x04\x5e\x13\x00\x4f\x20\x3c\x02\x72\x09\x4c\x27\x40\x1e\x41\x7a\x04\x6c\x13\x38\x4f\x00\x3e\x02\x79\x09\x68\x27\x30\x1f\x01\x7e\x04\x7a\x13\x70\x4f\x60\x3f\x02\x00\x0a\x04\x28\x20\x20\x41\x01\x05\x08\x14\x28\x50\x40\x41\x02\x07\x0a\x20\x28\x10\x21\x01\x05\x05\x16\x14\x60\x50\x20\x43\x02\x0e\x0a\x3c\x28\x00\x22\x41\x08\x05\x24\x14\x18\x51\x00\x45\x02\x15\x0a\x58\x28\x70\x22\x01\x0c\x05\x32\x14\x50\x51\x60\x46\x02\x1c\x0a\x74\x28\x60\x23\x41\x0f\x05\x40\x14\x68\x72\x60\x4b\x03\x30\x0e\x44\x39\x20\x66\x41\x19\x07\x68\x1c\x28\x73\x40\x4d\x03\x37\x0e\x60\x39\x10\x67\x01\x1d\x07\x76\x1c\x60\x73\x20\x4f\x03\x3e\x0e\x7c\x39\x00\x68\x41\x20\x07\x04\x1d\x18\x74\x00\x51\x03\x45\x0e\x18\x3a\x70\x68\x01\x24\x07\x12\x1d\x50\x74\x60\x52\x03\x4c\x0e\x34\x3a\x60\x69\x41\x27\x07\x20\x1d\x08\x75\x40\x54\x03\x53\x0e\x50\x3a\x50\x6a\x01\x2b\x07\x2e\x1d\x40\x75\x20\x56\x03\x5a\x0e\x6c\x3a\x40\x6b\x41\x2e\x07\x3c\x1d\x78\x75\x00\x58\x03\x61\x0e\x08\x3b\x30\x6c\x01\x32\x07\x4a\x1d\x30\x76\x60\x59\x03\x68\x0e\x24\x3b\x20\x6d\x41\x35\x07\x58\x1d\x68\x76\x40\x5b\x03\x6f\x0e\x0c\x2b\x40\x2c\x41\x32\x05\x4c\x15\x38\x56\x00\x5a\x02\x69\x0a\x28\x2b\x30\x2d\x01\x36\x05\x5a\x15\x70\x56\x60\x5b\x02\x70\x0a\x44\x2b\x20\x2e\x41\x39\x05\x68\x15\x28\x57\x40\x5d\x02\x77\x0a\x60\x2b\x10\x2f\x01\x3d\x05\x76\x15\x60\x57\x20\x5f\x02\x7e\x0a\x7c\x2b\x00\x30\x41\x40\x05\x04\x16\x18\x58\x00\x61\x02\x05\x0b\x18\x2c\x70\x30\x01\x44\x05\x12\x16\x50\x58\x60\x62\x02\x0c\x0b\x34\x2c\x60\x31\x41\x47\x05\x20\x16\x08\x59\x40\x64\x02\x13\x0b\x50\x2c\x50\x32\x01\x4b\x05\x2e\x16\x40\x59\x20\x66\x02\x1a\x0b\x6c\x2c\x40\x33\x41\x4e\x05\x3c\x16\x78\x59\x00\x68\x02\x21\x0b\x08\x2d\x30\x34\x01\x52\x05\x4a\x16\x30\x5a\x60\x69\x02\x70\x0e\x48\x3b\x30\x6e\x01\x3a\x07\x6a\x1d\x30\x77\x60\x5d\x03\x78\x0e\x64\x3b\x20\x6f\x41\x3d\x07\x78\x1d\x68\x77\x40\x5f\x03\x7f\x0e\x00\x3c\x10\x70\x01\x41\x07\x06\x1e\x20\x78\x20\x61\x03\x06\x0f\x1c\x3c\x00\x71\x41\x44\x07\x14\x1e\x58\x78\x00\x63\x03\x0d\x0f\x38\x3c\x60\x38\x41\x63\x05\x10\x17\x48\x5c\x40\x72\x02\x4b\x0b\x30\x2e\x50\x39\x01\x67\x05\x1e\x17\x00\x5d\x20\x74\x02\x52\x0b\x4c\x2e\x40\x3a\x41\x6a\x05\x2c\x17\x38\x5d\x00\x76\x02\x59\x0b\x68\x2e\x30\x3b\x01\x6e\x05\x3a\x17\x70\x5d\x60\x77\x02\x60\x0b\x04\x2f\x20\x3c\x41\x71\x05\x48\x17\x28\x5e\x40\x79\x02\x67\x0b\x20\x2f\x10\x3d\x01\x75\x05\x56\x17\x60\x5e\x20\x7b\x02\x6e\x0b\x3c\x2f\x00\x3e\x41\x78\x05\x64\x17\x78\x78\x20\x64\x03\x12\x0f\x4c\x3c\x40\x72\x41\x4a\x07\x2c\x1e\x38\x79\x00\x66\x03\x19\x0f\x68\x3c\x30\x73\x01\x4e\x07\x3a\x1e\x70\x79\x60\x67\x03\x20\x0f\x04\x3d\x20\x74\x41\x51\x07\x48\x1e\x28\x7a\x40\x69\x03\x27\x0f\x00\x00\x10\x00\x00\x01\x00\x06\x00\x20\x00\x20\x01\x00\x06\x00\x1c\x00\x00\x01\x00\x0a\x06\x2a\x18\x30\x61\x60\x05\x03\x18\x0c\x64\x30\x20\x43\x41\x0d\x06\x38\x18\x68\x61\x40\x07\x03\x1f\x0c\x00\x31\x10\x44\x01\x11\x06\x46\x18\x20\x62\x20\x09\x03\x26\x0c\x1c\x31\x00\x45\x41\x14\x06\x54\x18\x58\x62\x00\x0b\x03\x2d\x0c\x38\x31\x70\x45\x01\x18\x06\x62\x18\x10\x63\x60\x0c\x03\x34\x0c\x54\x31\x60\x46\x41\x1b\x06\x70\x18\x48\x63\x40\x0e\x03\x3b\x0c\x70\x31\x50\x47\x01\x1f\x06\x7e\x18\x00\x64\x20\x10\x03\x42\x0c\x0c\x32\x40\x48\x41\x22\x06\x0c\x19\x38\x64\x00\x12\x03\x49\x0c\x28\x32\x30\x49\x01\x26\x06\x1a\x19\x70\x64\x60\x13\x03\x50\x3a\x02",
        b"\x00\x32\x0d\x49\x3f\x00\x40\x00\x71\x07\x4b\x77\x11\x7e\x00\x00\x06\x22\x19\x10\x65\x60\x14\x03\x54\x0c\x54\x32\x60\x4a\x41\x2b\x06\x30\x19\x48\x65\x40\x16\x03\x5b\x0c\x70\x32\x50\x4b\x01\x2f\x06\x3e\x19\x00\x66\x20\x18\x03\x62\x0c\x0c\x33\x40\x4c\x41\x32\x06\x4c\x19\x38\x66\x00\x1a\x03\x69\x0c\x28\x33\x30\x4d\x01\x36\x06\x5a\x19\x70\x66\x60\x1b\x03\x70\x0c\x44\x33\x20\x4e\x41\x39\x06\x68\x19\x28\x67\x40\x1d\x03\x77\x0c\x60\x33\x10\x4f\x01\x3d\x06\x76\x19\x60\x67\x20\x1f\x03\x7e\x0c\x7c\x33\x00\x50\x41\x40\x06\x04\x1a\x18\x68\x00\x21\x03\x05\x0d\x18\x34\x70\x50\x01\x44\x06\x12\x1a\x50\x68\x60\x22\x03\x0c\x0d\x34\x34\x60\x51\x41\x47\x06\x20\x1a\x08\x69\x40\x24\x03\x13\x0d\x50\x34\x50\x52\x01\x4b\x06\x2e\x1a\x40\x69\x20\x26\x03\x1a\x0d\x6c\x34\x40\x53\x41\x4e\x06\x3c\x1a\x78\x69\x00\x28\x03\x21\x0d\x08\x35\x30\x54\x01\x52\x06\x4a\x1a\x30\x6a\x60\x29\x03\x28\x0d\x24\x35\x20\x55\x41\x55\x06\x58\x1a\x68\x6a\x40\x2b\x03\x2f\x0d\x40\x35\x10\x56\x01\x59\x06\x66\x1a\x20\x6b\x20\x2d\x03\x36\x0d\x5c\x35\x00\x57\x41\x5c\x06\x74\x1a\x58\x6b\x00\x2f\x03\x3d\x0d\x78\x35\x70\x57\x01\x60\x06\x02\x1b\x10\x6c\x60\x30\x03\x44\x0d\x14\x36\x60\x58\x41\x63\x06\x10\x1b\x48\x6c\x40\x32\x03\x4b\x0d\x30\x36\x50\x59\x01\x67\x06\x1e\x1b\x00\x6d\x20\x34\x03\x52\x0d\x4c\x36\x40\x5a\x41\x6a\x06\x2c\x1b\x38\x6d\x00\x36\x03\x59\x0d\x68\x36\x30\x5b\x01\x6e\x06\x3a\x1b\x70\x6d\x60\x37\x03\x60\x0d\x04\x37\x20\x5c\x41\x71\x06\x48\x1b\x28\x6e\x40\x39\x03\x67\x0d\x20\x37\x00\x00\x00\x30\x04\x42\x11\x10\x46\x60\x18\x02\x64\x08\x14\x23\x60\x0c\x41\x33\x04\x50\x11\x48\x46\x40\x1a\x02\x6b\x08\x24\x37\x20\x5d\x41\x75\x06\x58\x1b\x68\x6e\x40\x3b\x03\x6f\x0d\x40\x37\x10\x5e\x01\x79\x06\x66\x1b\x20\x6f\x20\x3d\x03\x76\x0d\x5c\x37\x00\x5f\x41\x7c\x06\x74\x1b\x58\x6f\x00\x3f\x03\x7d\x0d\x78\x37\x70\x5f\x01\x00\x07\x02\x1c\x10\x70\x60\x40\x03\x04\x0e\x14\x38\x60\x60\x41\x03\x07\x10\x1c\x48\x70\x40\x42\x03\x0e\x09\x3c\x24\x00\x12\x41\x48\x04\x24\x12\x18\x49\x00\x25\x02\x15\x09\x58\x24\x70\x12\x01\x4c\x04\x32\x12\x50\x49\x60\x26\x02\x1c\x09\x74\x24\x60\x13\x41\x4f\x04\x40\x12\x08\x4a\x40\x28\x02\x23\x09\x10\x25\x50\x14\x01\x53\x04\x4e\x12\x40\x4a\x20\x2a\x02\x2a\x09\x2c\x25\x40\x15\x41\x56\x04\x5c\x12\x78\x4a\x00\x2c\x02\x0b\x0e\x34\x38\x60\x61\x41\x07\x07\x20\x1c\x08\x71\x40\x44\x03\x13\x0e\x50\x38\x50\x62\x01\x0b\x07\x2e\x1c\x40\x71\x20\x46\x03\x1a\x0e\x6c\x38\x40\x63\x41\x0e\x07\x3c\x1c\x78\x71\x00\x48\x03\x21\x0e\x08\x39\x30\x64\x01\x12\x07\x4a\x1c\x30\x72\x60\x49\x03\x28\x0e\x24\x39\x20\x65\x41\x15\x07\x58\x1c\x10\x4d\x60\x34\x02\x54\x09\x54\x26\x60\x1a\x41\x6b\x04\x30\x13\x48\x4d\x40\x36\x02\x5b\x09\x70\x26\x50\x1b\x01\x6f\x04\x3e\x13\x00\x4e\x20\x38\x02\x62\x09\x0c\x27\x40\x1c\x41\x72\x04\x4c\x13\x38\x4e\x00\x3a\x02\x69\x09\x28\x27\x30\x1d\x01\x76\x04\x5a\x13\x70\x4e\x60\x3b\x02\x70\x09\x44\x27\x20\x1e\x41\x79\x04\x68\x13\x28\x4f\x40\x3d\x02\x77\x09\x60\x27\x10\x1f\x01\x7d\x04\x76\x13\x60\x4f\x20\x3f\x02\x7e\x09\x7c\x27\x00\x20\x41\x00\x05\x04\x14\x18\x50\x00\x41\x02\x05\x0a\x18\x28\x70\x20\x01\x04\x05\x12\x14\x50\x50\x60\x42\x02\x0c\x0a\x34\x28\x60\x21\x41\x07\x05\x20\x14\x08\x51\x40\x44\x02\x13\x0a\x50\x28\x50\x22\x01\x0b\x05\x2e\x14\x40\x51\x20\x46\x02\x1a\x0a\x6c\x28\x40\x23\x41\x0e\x05\x3c\x14\x78\x51\x00\x48\x02\x2d\x0e\x3c\x39\x00\x66\x41\x18\x07\x64\x1c\x18\x73\x00\x4d\x03\x35\x0e\x58\x39\x70\x66\x01\x1c\x07\x72\x1c\x50\x73\x60\x4e\x03\x3c\x0e\x74\x39\x60\x67\x41\x1f\x07\x00\x1d\x08\x74\x40\x50\x03\x43\x0e\x10\x3a\x50\x68\x01\x23\x07\x0e\x1d\x40\x74\x20\x52\x03\x4a\x0e\x2c\x3a\x40\x69\x41\x26\x07\x1c\x1d\x78\x74\x00\x54\x03\x51\x0e\x48\x3a\x30\x6a\x01\x2a\x07\x2a\x1d\x30\x75\x60\x55\x03\x58\x0e\x64\x3a\x20\x6b\x41\x2d\x07\x38\x1d\x68\x75\x40\x57\x03\x5f\x0e\x00\x3b\x10\x6c\x01\x31\x07\x46\x1d\x20\x76\x20\x59\x03\x66\x0e\x1c\x3b\x00\x6d\x41\x34\x07\x54\x1d\x58\x76\x00\x5b\x03\x6d\x0e\x38\x3b\x70\x6d\x41\x31\x05\x48\x15\x28\x56\x40\x59\x02\x67\x0a\x20\x2b\x10\x2d\x01\x35\x05\x56\x15\x60\x56\x20\x5b\x02\x6e\x0a\x3c\x2b\x00\x2e\x41\x38\x05\x64\x15\x18\x57\x00\x5d\x02\x75\x0a\x58\x2b\x70\x2e\x01\x3c\x05\x72\x15\x50\x57\x60\x5e\x02\x7c\x0a\x74\x2b\x60\x2f\x41\x3f\x05\x00\x16\x08\x58\x40\x60\x02\x03\x0b\x10\x2c\x50\x30\x01\x43\x05\x0e\x16\x40\x58\x20\x62\x02\x0a\x0b\x2c\x2c\x40\x31\x41\x46\x05\x1c\x16\x78\x58\x00\x64\x02\x11\x0b\x48\x2c\x30\x32\x01\x4a\x05\x2a\x16\x30\x59\x60\x65\x02\x18\x0b\x64\x2c\x20\x33\x41\x4d\x05\x38\x16\x68\x59\x40\x67\x02\x1f\x0b\x00\x2d\x10\x34\x01\x51\x05\x46\x16\x20\x5a\x20\x69\x02\x26\x0b\x1c\x2d\x00\x6e\x01\x39\x07\x66\x1d\x20\x77\x20\x5d\x03\x76\x0e\x5c\x3b\x00\x6f\x41\x3c\x07\x74\x1d\x58\x77\x00\x5f\x03\x7d\x0e\x78\x3b\x70\x6f\x01\x40\x07\x02\x1e\x10\x78\x60\x60\x03\x04\x0f\x14\x3c\x60\x70\x41\x43\x07\x32\x03",
        b"\x00\x32\x0d\x31\x26\x00\x40\x00\x62\x0f\x4b\x77\x61\x4b\x00\x00\x08\x0f\x24\x3c\x20\x71\x41\x45\x07\x18\x1e\x68\x78\x40\x63\x03\x46\x0b\x1c\x2e\x00\x39\x41\x64\x05\x14\x17\x58\x5c\x00\x73\x02\x4d\x0b\x38\x2e\x70\x39\x01\x68\x05\x22\x17\x10\x5d\x60\x74\x02\x54\x0b\x54\x2e\x60\x3a\x41\x6b\x05\x30\x17\x48\x5d\x40\x76\x02\x5b\x0b\x70\x2e\x50\x3b\x01\x6f\x05\x3e\x17\x00\x5e\x20\x78\x02\x62\x0b\x0c\x2f\x40\x3c\x41\x72\x05\x4c\x17\x38\x5e\x00\x7a\x02\x69\x0b\x28\x2f\x30\x3d\x01\x76\x05\x5a\x17\x70\x5e\x60\x7b\x02\x70\x0b\x44\x2f\x20\x3e\x41\x47\x07\x22\x1e\x10\x79\x60\x64\x03\x14\x0f\x54\x3c\x60\x72\x41\x4b\x07\x30\x1e\x48\x79\x40\x66\x03\x1b\x0f\x70\x3c\x50\x73\x01\x4f\x07\x3e\x1e\x00\x7a\x20\x68\x03\x22\x0f\x0c\x3d\x40\x74\x41\x52\x07\x4c\x1e\x38\x7a\x00\x00\x00\x01\x00\x08\x00\x30\x00\x00\x02\x00\x0a\x00\x30\x00\x60\x01\x00\x08\x00\x50\x30\x50\x42\x01\x0b\x06\x2e\x18\x40\x61\x20\x06\x03\x1a\x0c\x6c\x30\x40\x43\x41\x0e\x06\x3c\x18\x78\x61\x00\x08\x03\x21\x0c\x08\x31\x30\x44\x01\x12\x06\x4a\x18\x30\x62\x60\x09\x03\x28\x0c\x24\x31\x20\x45\x41\x15\x06\x58\x18\x68\x62\x40\x0b\x03\x2f\x0c\x40\x31\x10\x46\x01\x19\x06\x66\x18\x20\x63\x20\x0d\x03\x36\x0c\x5c\x31\x00\x47\x41\x1c\x06\x74\x18\x58\x63\x00\x0f\x03\x3d\x0c\x78\x31\x70\x47\x01\x20\x06\x02\x19\x10\x64\x60\x10\x03\x44\x0c\x14\x32\x60\x48\x41\x23\x06\x10\x19\x48\x64\x40\x12\x03\x4b\x0c\x30\x32\x50\x49\x01\x27\x06\x1e\x19\x00\x65\x20\x14\x03\x52\x0c\x4c\x32\x40\x4a\x41\x2a\x06\x2c\x19\x38\x65\x00\x16\x03\x59\x0c\x68\x32\x30\x4b\x01\x2e\x06\x3a\x19\x70\x65\x20\x02\x00\x0b\x00\x30\x00\x50\x01\x00\x07\x00\x1e\x00\x00\x01\x20\x04\x00\x12\x00\x4c\x00\x40\x02\x40\x0a\x00\x2c\x00\x38\x01\x00\x06\x00\x19\x00\x68\x00\x30\x03\x00\x0e\x00\x3a\x00\x70\x01\x60\x07\x00\x20\x00\x04\x01\x20\x04\x40\x11\x00\x48\x00\x28\x02\x40\x09\x00\x27\x00\x20\x01\x10\x05\x00\x15\x00\x56\x00\x60\x02\x20\x0b\x00\x2e\x00\x3c\x01\x00\x06\x40\x18\x00\x64\x00\x18\x03\x00\x0d\x00\x35\x00\x58\x01\x70\x06\x00\x1c\x00\x72\x00\x50\x03\x60\x0e\x00\x3c\x00\x74\x01\x60\x07\x40\x1f\x00\x00\x01\x08\x04\x40\x10\x00\x43\x00\x10\x02\x50\x08\x00\x23\x00\x0e\x01\x40\x04\x20\x12\x00\x4a\x00\x2c\x02\x40\x09\x40\x26\x00\x1c\x01\x78\x04\x00\x14\x00\x51\x00\x48\x02\x00\x55\x41\x54\x06\x54\x1a\x58\x6a\x00\x2b\x03\x2d\x0d\x38\x35\x70\x55\x01\x58\x06\x62\x1a\x10\x6b\x60\x2c\x03\x34\x0d\x54\x35\x60\x56\x41\x5b\x06\x70\x1a\x48\x6b\x40\x2e\x03\x3b\x0d\x70\x35\x50\x57\x01\x5f\x06\x7e\x1a\x00\x6c\x20\x30\x03\x42\x0d\x0c\x36\x40\x58\x41\x62\x06\x0c\x1b\x38\x6c\x00\x32\x03\x49\x0d\x28\x36\x30\x59\x01\x66\x06\x1a\x1b\x70\x6c\x60\x33\x03\x50\x0d\x44\x36\x20\x5a\x41\x69\x06\x28\x1b\x28\x6d\x40\x35\x03\x57\x0d\x60\x36\x10\x5b\x01\x6d\x06\x36\x1b\x60\x6d\x20\x37\x03\x5e\x0d\x7c\x36\x00\x5c\x41\x70\x06\x44\x1b\x18\x6e\x00\x39\x03\x65\x0d\x18\x37\x70\x5c\x01\x74\x06\x00\x00\x60\x76\x6d\x1b\x38\x65\x64\x01\x18\x7f\x12"]

pedal = twinlooper.twinlooper()

outfile = open("info_from_log.bin", "wb")
for info in infos:
    blen = (info[5]*128*128) + (info[4]*128) + info[3]
    rsp = pedal.unpack(bytes(info)[8:], blen)

    print(hexdump(rsp[:64]))

    dlen = (rsp[6]*256*256) + (rsp[5]*256) + rsp[4]
    outfile.write(rsp[7:7 + dlen])

outfile.close()
