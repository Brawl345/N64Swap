#!/usr/bin/env python3
import os
from argparse import ArgumentParser

import numpy

valid_ext = [".n64", ".v64", ".z64"]
parser = ArgumentParser()
parser.add_argument('input', type=str, help="Input File")
parser.add_argument('output', type=str, help="Output File")
arguments = parser.parse_args()


def read_in_chunks(file_object, chunk_size=1024):
    """Lazy function (generator) to read a file piece by piece.
    Default chunk size: 1k."""
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data


def get_rom_format(rom_header):
    if rom_header == b"\x40\x12\x37\x80":
        return ".n64"
    elif rom_header == b"\x80\x37\x12\x40":
        return ".z64"
    elif rom_header == b"\x37\x80\x40\x12":
        return ".v64"
    else:
        return None


def swap_bytes(b):
    chunk_bytearray = bytearray(b)
    byteswapped = bytearray(len(b))
    byteswapped[0::2] = chunk_bytearray[1::2]
    byteswapped[1::2] = chunk_bytearray[0::2]
    return byteswapped


def main(infile, outfile):
    # TODO: check if input == output

    output_ext = os.path.splitext(outfile)[1]
    if output_ext.lower() not in valid_ext:
        print("Output file must end with .n64, .v64 or .z64")
        return

    with open(infile, "rb") as rom_file:
        rom_header = rom_file.read(4)
        rom_format = get_rom_format(rom_header)
        if not rom_format:
            print("Not an N64 rom.")
            return
        rom_file.seek(0)

        print("{0} -> {1}".format(rom_format, output_ext))
        with open(outfile, "wb") as out_file:
            if rom_format == output_ext:  # Just copy it
                for chunk in read_in_chunks(rom_file):
                    out_file.write(chunk)

            if rom_format == ".z64":  # Big Endian
                if output_ext == ".n64":  # Big Endian -> Little Endian
                    for chunk in read_in_chunks(rom_file):
                        out_file.write(numpy.frombuffer(chunk, numpy.float32).byteswap())
                elif output_ext == ".v64":  # Big Endian -> Byteswapped
                    for chunk in read_in_chunks(rom_file):
                        out_file.write(swap_bytes(chunk))

            elif rom_format == ".n64":  # Little Endian
                if output_ext == ".z64":  # Little Endian -> Big Endian
                    for chunk in read_in_chunks(rom_file):
                        out_file.write(numpy.frombuffer(chunk, numpy.float32).byteswap())
                elif output_ext == ".v64":  # Little Endian -> Big Endian -> Byteswapped
                    for chunk in read_in_chunks(rom_file):
                        endian_swapped = numpy.frombuffer(chunk, numpy.float32).byteswap()
                        out_file.write(swap_bytes(endian_swapped.tobytes()))

            elif rom_format == ".v64":  # Byteswapped
                if output_ext == ".n64":  # Byteswapped -> Big Endian -> Little Endian
                    for chunk in read_in_chunks(rom_file):
                        endian_swapped = numpy.frombuffer(chunk, numpy.float32).byteswap()
                        out_file.write(swap_bytes(endian_swapped.tobytes()))
                elif output_ext == ".z64":  # Byteswapped -> Big Endian
                    for chunk in read_in_chunks(rom_file):
                        out_file.write(swap_bytes(chunk))

    print("Conversion finished.")


if __name__ == "__main__":
    main(infile=arguments.input, outfile=arguments.output)
