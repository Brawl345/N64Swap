N64Swap
=======
Swaps .n64, .v64 and .z64 roms. Written in Python 3. You must install `numpy` via e.g. pip. Code is kinda messy.

## Usage
```
n64swap.py [-h] input output
```

## Technical information
`.z64` is the correct format and should be used. This handy table shows the [difference](https://old.reddit.com/r/emulation/comments/7hrvzp/the_three_different_n64_rom_formats_explained_for/):

| ROM format | Type          | First 4 bytes | Game Title in ROM  |
|------------|---------------|---------------|--------------------|
| .z64       | Big Endian    | 80 37 12 40   | `SUPER MARIO 64  ` |
| .v64       | Byteswapped   | 37 80 40 12   | `USEP RAMIR O64  ` |
| .n64       | Little Endian | 40 12 37 80   | `EPUSAM R OIR  46` |

(Note that there are two spaces after both "64", they don't seem to show up here.)