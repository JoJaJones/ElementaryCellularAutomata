from RuleBuilder import RuleBuilder, MAX_ROWS


WHITE = "WHITE"
RED = "RED"
GREEN = "GREEN"
YELLOW = "YELLOW"
BLUE = "BLUE"
PURPLE = "PURPLE"
TEAL = "TEAL"
GRAY = "GRAY"
LIGHT_GRAY = f"LIGHT_{GRAY}"
LIGHT_RED = f"LIGHT_{RED}"
LIGHT_GREEN = f"LIGHT_{GREEN}"
LIGHT_YELLOW = f"LIGHT_{YELLOW}"
LIGHT_BLUE = f"LIGHT_{BLUE}"
LIGHT_PURPLE = f"LIGHT_{PURPLE}"
LIGHT_TEAL = f"LIGHT_{TEAL}"
BLACK = "BLACK"
CLEAR = "CLEAR"
COLORS_LIST = [WHITE, RED, GREEN, YELLOW, BLUE, PURPLE, TEAL, GRAY, LIGHT_GRAY, LIGHT_RED, LIGHT_GREEN, LIGHT_YELLOW,
               LIGHT_BLUE, LIGHT_PURPLE, LIGHT_TEAL, BLACK]
COLOR_DICT = {WHITE: 40, RED: 41, GREEN: 42, YELLOW: 43, BLUE: 44, PURPLE: 45, TEAL: 46, LIGHT_GRAY: 47,
              GRAY: 100, LIGHT_RED: 101, LIGHT_GREEN: 102, LIGHT_YELLOW: 103, LIGHT_BLUE: 104, LIGHT_PURPLE: 105,
              LIGHT_TEAL: 106, BLACK: 107, CLEAR: 0}


class RulePrinter:
    def __init__(self, num_colors, color_list):
        self._color_dict = {}
        self._num_colors = num_colors
        self._cur_color = CLEAR
        self._color_list = color_list
        self._load_color_dict()

    def _load_color_dict(self):
        for i in range(len(self._color_list)):
            self._color_dict[self._color_list[i]] = f"\033[{COLOR_DICT[self._color_list[i]]}m"

        if BLACK not in self._color_list and len(self._color_list) > 2:
            self._color_dict[BLACK] = f"\033[{COLOR_DICT[BLACK]}m"

    def print_rule(self, rule_list):
        rule_str = ""
        for r in range(len(rule_list)):
            rule_str += self._print_line(rule_list[r], r)
        
        return rule_str

    def _print_line(self, row, row_num):
        line_str = ""
        for c in range(len(row)):
            if self._num_colors > 2:
                if row[c] == 1 and self._cur_color == self._color_list[0]:
                    self._cur_color = self._calc_color(row, row_num, c)
                elif row[c] == 0:
                    self._cur_color = self._color_list[0]
                else:
                    self._cur_color = CLEAR
            else:
                if row[c] == -1:
                    self._cur_color = CLEAR
                else:
                    self._cur_color = self._color_list[row[c]]

            line_str += f"\033[{COLOR_DICT[self._cur_color]}m  "

        return line_str + f"\033[{COLOR_DICT[CLEAR]}m" + "\n"

    def print_rule_mirror(self, rule_list):
        mirror_str = ""
        for i in range(-1, -(len(rule_list)), -1):
            mirror_str += self._print_line(rule_list[i], len(rule_list) - 1)

        mirror_str += self.print_rule(rule_list)

        return mirror_str

    def _calc_color(self, rule_list, r, c):
        return self._color_list[rule_list[r][c]]

