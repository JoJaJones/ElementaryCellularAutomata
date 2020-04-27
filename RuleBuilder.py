from math import log2
MAX_ROWS = 20

class RuleBuilder:
    def __init__(self, rule_number: int, rule_size: int = 8):
        self._rule_size = rule_size
        self._tuple_size = int(log2(rule_size))
        self._true_configs = self._load_truths(rule_number)
        self._rule_results = []
        self._cur_row = 0


    def _load_truths(self, rule_number: int) -> list:
        bits = []
        i = 1
        for x in range(1, self._rule_size):
            if rule_number & i:
                bits.append(x - 1)

            i <<= 1

        rules = []
        for bit in bits:
            cur_rule = []
            for shift in range(self._tuple_size):
                two_pow = 1 << shift
                cur_rule = [((bit & two_pow) >> (shift))] + cur_rule

            rules.append(tuple(cur_rule))

        return rules

    def build_rule(self):
        for i in range(MAX_ROWS + 1):
            self.build_next_line()

        for row in self._rule_results:
            row[0] = row[-1] = 0

        self._rule_results[-1] = [0 for x in range(MAX_ROWS * 2 + 1)]

        return self._rule_results

    def build_next_line(self):
        if self._cur_row == MAX_ROWS + 1:
            self._cur_row = 0
            self._rule_results = []

        cur_row_idx = self._cur_row

        min_idx = MAX_ROWS - (cur_row_idx)
        max_idx = MAX_ROWS + (cur_row_idx)
        self._rule_results.append([-1 for x in range(MAX_ROWS * 2 + 1)])
        cur_row = self._rule_results[-1]
        if cur_row_idx == 0:
            cur_row[MAX_ROWS] = 1
            for i in range(min_idx, max_idx + 1):
                if i != MAX_ROWS:
                    self._set_cell(0, i, 0)
        else:
            for i in range(cur_row_idx):
                if i == 0 and cur_row_idx:
                    self._set_cell(0, min_idx, 0)
                    self._set_cell(0, max_idx, 0)

            for i in range(self._cur_row + 1):
                self._set_cell(self._cur_row, MAX_ROWS + i)
                if i != 0:
                    self._set_cell(self._cur_row, MAX_ROWS - i)

        self._cur_row += 1

        return self._rule_results

    def _set_cell(self, row_idx: int, idx: int, value: int = None) -> None:
        if 0 <= idx <= 2 * MAX_ROWS:
            if value is None:
                if self._gen_tuple(row_idx - 1, idx) in self._true_configs:
                    self._rule_results[row_idx][idx] = 1
                else:
                    self._rule_results[row_idx][idx] = 0
            else:
                self._rule_results[row_idx][idx] = 0

    def _gen_tuple(self, row: int, idx: int) -> tuple:
        vals = []
        idx_shift = self._tuple_size//2
        for i in range(idx - idx_shift, idx + idx_shift + 1):
            if i < 0 or i > MAX_ROWS * 2:
                vals.append(-1)
            else:
                vals.append(self._rule_results[row][i])

        for i in range(len(vals)):
            if vals[i] == -1:
                if row > 0:
                    self._set_cell(row, idx + i - idx_shift)
                elif row == 0:
                    self._set_cell(row, idx + i - idx_shift, 0)

                if 0 <= idx + i - idx_shift <= 2 * MAX_ROWS:
                    vals[i] = self._rule_results[row][idx + i - idx_shift]
                else:
                    vals[i] = vals[self._tuple_size // 2]

        return tuple(vals)
