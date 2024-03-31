VARINT_DATA_BYTE_BITS = 0x7F  # 0b0111 1111
VARINT_EXISTS_NEXT_BYTE_BIT = 0x80  # 0b1000 0000


def varint_encode(encode_val):
    byte_arr = bytearray()
    while True:
        varint_byte = encode_val & VARINT_DATA_BYTE_BITS
        rest_val = encode_val >> 7
        byte_arr.append(varint_byte)
        if not rest_val:
            break
        encode_val = rest_val

    # if comment below line, change to small endian mode
    # byte_arr.reverse() # big endian mode
    for offset, byte in enumerate(byte_arr):
        if offset + 1 == len(byte_arr):
            # last byte
            break
        byte_arr[offset] = byte_arr[offset] | VARINT_EXISTS_NEXT_BYTE_BIT

    return byte_arr


def varint_decode(varint_byte_arr):
    # type: (bytearray) -> int
    # change to big endian sequence which human can understand
    varint_byte_arr.reverse()

    decode_val = 0x0
    for offset, byte in enumerate(varint_byte_arr):
        byte_data = byte & VARINT_DATA_BYTE_BITS
        decode_val = decode_val + byte_data

        if offset + 1 == len(varint_byte_arr):
            # last byte
            break
        else:
            decode_val = decode_val << 7

    return decode_val


def test_varint():
    varint_test_list = [1337, 1235, 99976, 12, 45]
    for test_val in varint_test_list:
        encoded = varint_encode(test_val)
        print('encoded of {}: {}'.format(test_val, ' '.join(map(bin, encoded))))
        print('decode: {}'.format(varint_decode(encoded)))


if __name__ == '__main__':
    test_varint()

# output of big endian mode
# encoded of 1337: 0b10001010 0b111001
# decode: 1337
# encoded of 1235: 0b10001001 0b1010011
# decode: 1235
# encoded of 99976: 0b10000110 0b10001101 0b1000
# decode: 99976
# encoded of 12: 0b1100
# decode: 12
# encoded of 45: 0b101101
# decode: 45

# output of small endian mode
# encoded of 1337: 0b10111001 0b1010
# decode: 1337
# encoded of 1235: 0b11010011 0b1001
# decode: 1235
# encoded of 99976: 0b10001000 0b10001101 0b110
# decode: 99976
# encoded of 12: 0b1100
# decode: 12
# encoded of 45: 0b101101
# decode: 45
