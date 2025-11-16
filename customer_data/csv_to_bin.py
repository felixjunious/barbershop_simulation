import csv
import struct

FMT = "20s"

def pack_record(name, fmt=FMT):
    size = struct.calcsize(fmt)
    name_bytes = name.strip().encode()[:size]
    name_bytes = name_bytes.ljust(size, b"\x00")
    return struct.pack(fmt, name_bytes)


def unpack_record(record_bytes, fmt=FMT):
    raw = struct.unpack(fmt, record_bytes)[0]
    return raw.decode().rstrip("\x00").strip()


def read_csv_to_list(file):
    lst = []
    with open(file, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            lst.append(row[0])
    return lst

def read_bin_to_list(file, fmt=FMT):
    lst = []
    size = struct.calcsize(fmt)

    with open(file, "rb") as f:
        while True:
            record_byte = f.read(size)
            if len(record_byte) < size:
                break

            lst.append(unpack_record(record_byte, fmt))

    return lst

def save_list_to_bin(lst, file, fmt=FMT):
    with open(file, "wb") as f:
        for elem in lst:
            record_byte = pack_record(elem, fmt)
            f.write(record_byte)


if __name__ == "__main__":
    names = read_csv_to_list("names_reshaped.csv")
    save_list_to_bin(names, "names.bin", FMT)

