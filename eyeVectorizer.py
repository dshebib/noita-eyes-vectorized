import sys
import math
import copy


eyeMap = {0: [0, 0],
          1: [0, 1],
          2: [1, 0],
          3: [0, -1],
          4: [-1, 0]
          }

vecEncodeMap = {
        (0.0, 0.0): 0,
        (0.0, 1.0): 1,
        (0.45, 0.89): 2,
        (0.71, 0.71): 3,
        (0.89, 0.45): 4,
        (1.0, 0.0): 5,
        (0.89, -0.45): 6,
        (0.71, -0.71): 7,
        (0.45, -0.89): 8,
        (0.0, -1.0): 9,
        (-0.45, -0.89): 10,
        (-0.71, -0.71): 11,
        (-0.89, -0.45): 12,
        (-1.0, 0.0): 13,
        (-0.89, 0.45): 14,
        (-0.71, 0.71): 15,
        (-0.45, 0.89): 16
                }

unicodeArrowMap = {
        0: '\u2022 ',
        1: '\u2191 ',
        2: '\u2197\u25B4',
        3: '\u2197 ',
        4: '\u2197\u25B8',
        5: '\u2192 ',
        6: '\u2198\u25B8',
        7: '\u2198 ',
        8: '\u2198\u25BE',
        9: '\u2193 ',
        10: '\u2199\u25BE',
        11: '\u2199 ',
        12: '\u2199\u25C2',
        13: '\u2190 ',
        14: '\u2196\u25C2',
        15: '\u2196 ',
        16: '\u2196\u25B4'
        }


def import_to_df(path: str):
    with open(path, 'r') as file:
        data = [[int(char) for char in line.strip()]
                for line in file.readlines()]

    return data


def print2(m):
    for r in m:
        print(r)


def isOdd(x: int) -> bool:
    return bool(x % 2)


def avg2d(vecs: list[list[int]]) -> list[float]:
    avgX = float(sum([x[0] for x in vecs]))/len(vecs)
    avgY = float(sum([x[1] for x in vecs]))/len(vecs)

    return [avgX, avgY]


def normalize(vec: list[float]) -> list[float]:
    mag: float = sum([v*v for v in vec])
    mag = math.sqrt(mag)

    if mag == 0:
        return vec
    factor: float = (1.0/mag)
    return [factor*v for v in vec]


def avg_trigrams(eyes):
    retVal: list[list[list: int]] = []
    rdx: int = 0

    while rdx < len(eyes):
        retVal.append([])
        tdx: int = 0

        while (int(tdx/2)*3+2) < len(eyes[rdx]):
            trigram: list[list: int] = []
            tidx: int = int(tdx/2) * 3
            if not isOdd(tdx):
                trigram.append(eyes[rdx][tidx])
                trigram.append(eyes[rdx][tidx + 1])
                trigram.append(eyes[rdx+1][tidx])

            else:
                trigram.append(eyes[rdx][tidx + 2])
                trigram.append(eyes[rdx+1][tidx + 1])
                trigram.append(eyes[rdx+1][tidx + 2])

            averaged: list[float] = avg2d(trigram)
            normalized = normalize(averaged)

            retVal[int(rdx/2)].append(normalized)
            tdx += 1

        rdx += 2

    return retVal


def flip_vec(vec: tuple[float, float]) -> tuple[float, float]:
    outVec: tuple(float, float) = (-1*vec[0], -1*vec[1])
    return outVec


def flip_alternating(vecs: list[tuple[float, float]]) -> None:
    for row in vecs:
        for i in range(0, len(row)):
            if not isOdd(i):
                row[i] = flip_vec(row[i])


def only_up(vecs):
    vecs_out = []
    for rdx, row in enumerate(vecs):
        vecs_out.append([])
        for i in range(0, len(row)):
            if not isOdd(i):
                vecs_out[rdx].append(row[i])

    return vecs_out


def only_down(vecs):
    vecs_out = []
    for rdx, row in enumerate(vecs):
        vecs_out.append([])
        for i in range(0, len(row)):
            if isOdd(i):
                vecs_out[rdx].append(row[i])

    return vecs_out


def decode_hex(vecs):
    s_dec: str = ""
    for r in vecs:
        for idx in range(0, len(r)-1, 2):
            c_int = int(str(r[idx]) + str(r[idx+1]))
            if 32 <= c_int and c_int <= 126:
                s_dec += chr(c_int)
        s_dec += "\\n"
    return s_dec


def unicodeArrows(vecs):
    s_dec: str = ""
    for r in vecs:
        s_dec += "  ".join([unicodeArrowMap[x] for x in r])
        s_dec += "\n\n"
    return s_dec


def main() -> int:
    filename: str = sys.argv[1]
    eyes = import_to_df(filename)

    eyes = [[eyeMap[x] for x in r] for r in eyes]

    eyes = avg_trigrams(eyes)

    eyes = [[tuple([round(x, 2) for x in v]) for v in r] for r in eyes]
    eyesReversed = copy.deepcopy(eyes)
    eyesUp = copy.deepcopy(eyes)
    eyesDown = copy.deepcopy(eyes)

    # encode
    eyes = [[vecEncodeMap[x] for x in r] for r in eyes]

    print(filename)
    print("output")

    hexStrings = ["".join([format(x, 'X') for x in r]) for r in eyes]
    print(hexStrings)

    print(decode_hex(eyes))
    print()

    print("reversed")
    print([s[::-1] for s in hexStrings])

    print("flipped")
    flip_alternating(eyesReversed)
    eyesReversed = [[vecEncodeMap[x] for x in r] for r in eyesReversed]
    hexStringsRev = ["".join([format(x, 'X') for x in r]) for r in eyesReversed]
    print(hexStringsRev)
    print(decode_hex(eyesReversed))
    print()

    print("flipped and reversed")
    print([s[::-1] for s in hexStringsRev])

    print("OnlyUp")
    eyesUp = only_up(eyesUp)
    eyesUp = [[vecEncodeMap[x] for x in r] for r in eyesUp]
    hexStringsUp = ["".join([format(x, 'X') for x in r]) for r in eyesUp]
    print(hexStringsUp)
    print(decode_hex(eyesUp))
    print()
    print("OnlyUp reversed")
    print([s[::-1] for s in hexStringsUp])

    print("OnlyDown")
    eyesDown = only_down(eyesDown)
    eyesDown = [[vecEncodeMap[x] for x in r] for r in eyesDown]
    hexStringsDown = ["".join([format(x, 'X') for x in r]) for r in eyesDown]
    print(hexStringsDown)
    print(decode_hex(eyesDown))
    print()
    print("OnlyDown reversed")
    print([s[::-1] for s in hexStringsDown])

    print()
    print(unicodeArrows(eyes))


if __name__ == '__main__':
    sys.exit(main())
