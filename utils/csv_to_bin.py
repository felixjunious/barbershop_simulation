"""
Convert a CSV file of names into a fixed-width binary file and provide utilities
to read/write binary records.

Binary format:
    - Each record is 20 bytes (default FMT="20s")
"""

import csv
import struct

# Default fixed-size format for each record
FMT = "20s"

def pack_record(name, fmt=FMT):
    """
    Pack a string name into a fixed-size binary record.

    Args:
        name (str): Name to pack.
        fmt (str): Struct format string (default "20s").

    Returns:
        bytes: Packed binary record of fixed size.
    """
    size = struct.calcsize(fmt)
    name_bytes = name.strip().encode()[:size]  # truncate if too long
    name_bytes = name_bytes.ljust(size, b"\x00")  # pad with null bytes
    return struct.pack(fmt, name_bytes)


def unpack_record(record_bytes, fmt=FMT):
    """
    Unpack a fixed-size binary record into a string.

    Args:
        record_bytes (bytes): Binary record bytes.
        fmt (str): Struct format string (default "20s").

    Returns:
        str: Decoded and stripped string.
    """
    raw = struct.unpack(fmt, record_bytes)[0]
    return raw.decode().rstrip("\x00").strip()


def read_csv_to_list(file):
    """
    Read a CSV file (single column) and return a list of names.

    Args:
        file (str): Path to the CSV file.

    Returns:
        list of str: List of names.
    """
    lst = []
    with open(file, "r", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            lst.append(row[0])
    return lst


def read_bin_to_list(file, fmt=FMT):
    """
    Read a binary file of fixed-size records and return a list of names.

    Args:
        file (str): Path to the binary file.
        fmt (str): Struct format string.

    Returns:
        list of str: List of decoded names.
    """
    lst = []
    size = struct.calcsize(fmt)

    with open(file, "rb") as f:
        while True:
            record_bytes = f.read(size)
            if len(record_bytes) < size:
                break
            lst.append(unpack_record(record_bytes, fmt))

    return lst


def save_list_to_bin(lst, file, fmt=FMT):
    """
    Save a list of strings into a fixed-width binary file.

    Args:
        lst (list of str): List of names to save.
        file (str): Path to the binary file.
        fmt (str): Struct format string.
    """
    with open(file, "wb") as f:
        for elem in lst:
            record_bytes = pack_record(elem, fmt)
            f.write(record_bytes)


if __name__ == "__main__":
    names = read_csv_to_list("../customer_data/names_reshaped.csv")
    save_list_to_bin(names, "../customer_data/names.bin", FMT)
    print(f"Saved {len(names)} names to '../customer_data/names.bin'")
