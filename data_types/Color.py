from __future__ import annotations
from multimethod import multimethod

class Color:
    @multimethod
    def __init__(self: Color):
        self.r = 0
        self.g = 0
        self.b = 0
        self.a = 1
    @multimethod
    def __init__(self: Color, _from: Color, alpha: float | int):
        self.r = _from.r
        self.g = _from.g
        self.b = _from.b
        self.a = alpha
    @multimethod
    def __init__(self: Color, _from: Color):
        self.r = _from.r
        self.g = _from.g
        self.b = _from.b
        self.a = _from.a
    @multimethod
    def __init__(self: Color, code: str):
        html(code)
    @multimethod
    def __init__(self: Color, code: str, alpha: float | int):
        html(code)
        self.a = alpha
    @multimethod
    def __init__(self: Color, r: float | int, g: float | int, b: float | int):
        self.r = r
        self.g = g
        self.b = b
        self.a = 1
    @multimethod
    def __init__(self: Color, r: float | int, g: float | int, b: float | int, a: float | int):
        self.r = r
        self.g = g
        self.b = b
        self.a = a
    def html(self, p_rgba):
        if p_rgba == "":
            self.r = 0
            self.g = 0
            self.b = 0
            self.a = 0
        else:
            current_pos = (p_rgba[0] == '#') and 1 or 0
            num_of_digits = len(p_rgba) - current_pos
            r, g, b, a = 1.0
            match num_of_digits:
                case 3:
                    r = int(p_rgba[current_pos+0], 16) / 15
                    g = int(p_rgba[current_pos+1], 16) / 15
                    b = int(p_rgba[current_pos+2], 16) / 15
                case 4:
                    r = int(p_rgba[current_pos+0], 16) / 15
                    g = int(p_rgba[current_pos+1], 16) / 15
                    b = int(p_rgba[current_pos+2], 16) / 15
                    a = int(p_rgba[current_pos+3], 16) / 15
                case 6:
                    r = int(p_rgba[current_pos+0:current_pos+2], 16) / 255
                    g = int(p_rgba[current_pos+2:current_pos+4], 16) / 255
                    b = int(p_rgba[current_pos+4:current_pos+6], 16) / 255
                case 8:
                    r = int(p_rgba[current_pos+0:current_pos+2], 16) / 255
                    g = int(p_rgba[current_pos+2:current_pos+4], 16) / 255
                    b = int(p_rgba[current_pos+4:current_pos+6], 16) / 255
                    a = int(p_rgba[current_pos+6:current_pos+8], 16) / 255
                case _:
                    print("Invalid color code: " + p_rgba + ".")
                    exit()
            self.r = r
            self.g = g
            self.b = b
            self.a = a
    def json(self):
        r = int(self.r*255)
        g = int(self.g*255)
        b = int(self.b*255)
        a = int(self.a*255)
        return f'{r:02x}{g:02x}{b:02x}{a:02x}'
