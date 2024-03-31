def zigzag_encode(int_val):
    """
     0 => 0
    -1 => 1
     1 => 2
    -2 => 3
     2 => 4
    -3 => 5
     3 => 6

    binary format:
    if origin is positive number, encoded number is origin*2, binary move left one bit
    1 -> 2 :  1 -> 10
    2 -> 4 : 10 -> 100
    3 -> 6 : 11 -> 110
    if origin is negative number, encoded number is origin*(-2)-1
    -1 -> 1 : -1 -> 1
    -2 -> 3 : -10 -> 11
    -3 -> 5 : -11 -> 101
    x = origin*2-1
    origin = (x+1)/2
    """
    if int_val >= 0:
        return int_val << 1
    else:
        return (abs(int_val) << 1) - 1


def zigzag_decode(zigzag_code):
    if zigzag_code % 2 == 0:
        return zigzag_code >> 1
    else:
        # return -(zigzag_code >> 1) - 1 # == -(zigzag_code+1)>>1
        return -(zigzag_code + 1)>>1 # == -(zigzag_code+1)>>1


def test_zigzag():
    zigzag_test = [0, -1, 1, -2, 2, -3, 3, 4, -4, 8, -8, 16, -16, 555, -555, 444, -444 - 123213]
    for original in zigzag_test:
        encode_val = zigzag_encode(original)
        print('encode: {} => {}'.format(original, encode_val))
        print('decode: {} => {}'.format(encode_val, zigzag_decode(encode_val)))


if __name__ == '__main__':
    test_zigzag()

# output
# encode: 0 => 0
# decode: 0 => 0
# encode: -1 => 1
# decode: 1 => -1
# encode: 1 => 2
# decode: 2 => 1
# encode: -2 => 3
# decode: 3 => -2
# encode: 2 => 4
# decode: 4 => 2
# encode: -3 => 5
# decode: 5 => -3
# encode: 3 => 6
# decode: 6 => 3
# encode: 4 => 8
# decode: 8 => 4
# encode: -4 => 7
# decode: 7 => -4
# encode: 8 => 16
# decode: 16 => 8
# encode: -8 => 15
# decode: 15 => -8
# encode: 16 => 32
# decode: 32 => 16
# encode: -16 => 31
# decode: 31 => -16
# encode: 555 => 1110
# decode: 1110 => 555
# encode: -555 => 1109
# decode: 1109 => -555
# encode: 444 => 888
# decode: 888 => 444
# encode: -123657 => 247313
# decode: 247313 => -123657