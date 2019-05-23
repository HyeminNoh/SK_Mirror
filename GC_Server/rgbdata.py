# 기본제공 컬러 데이터의 rgb데이터 모음
# 이미지 이름 기반으로 선택된 이미지의 rgb 튜플값을 반환

import json

default_color={
    "black": (0, 0, 0),
    "gray": (129, 128, 119),
    "babypink": (132, 79, 87),
    "pink": (115, 51, 79),
    "violet": (63, 44, 77),
    "lavendar": (120, 93, 137),
    "platinumaqua": (98, 108, 133),
    "platinummatt": (127, 145, 155),
    "mattkhaki": (92, 107, 97),
    "olive": (131, 128, 90),
    "brown": (156, 123, 91),
    "darkbrown": (28, 7, 0),
}

def find(colorName):
    rgbdata = (0,0,0)
    if colorName in default_color.keys():
        rgbdata = default_color[colorName]
    return rgbdata