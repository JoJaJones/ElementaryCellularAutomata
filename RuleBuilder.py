MAX_ROWS = 15

class RuleBuilder:
    def __init__(self, rule_number: int):
        self._true_configs = self._load_truths(rule_number)
        self._rule_results = []
        self._cur_row = 0


    def _load_truths(self, rule_number: int) -> list:
        bits = []
        i = 1
        for x in range(1, 9):
            if rule_number & i:
                bits.append(x - 1)

            i <<= 1

        rules = []
        for bit in bits:
            rule = ((bit & 4) >> 2, (bit & 2) >> 1, bit & 1)
            rules.append(rule)

        return rules

    def build_rule(self):
        for i in range(MAX_ROWS + 1):
            self.build_next_line()

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
        else:
            if cur_row_idx == 1:
                cur_row[MAX_ROWS - 1] = 0
                cur_row[MAX_ROWS + 1] = 0

            for i in range(cur_row_idx):
                if i == 0 and cur_row_idx:
                    self._set_cell(0, min_idx, 0)
                    self._set_cell(0, max_idx, 0)
                else:
                    self._set_cell(i, min_idx)
                    self._set_cell(i, max_idx)

            for i in range(self._cur_row + 1):
                self._set_cell(self._cur_row, MAX_ROWS + i)
                if i != 0:
                    self._set_cell(self._cur_row, MAX_ROWS - i)

        self._cur_row += 1

        return self._rule_results

    def _set_cell(self, row_idx: int, idx: int, value: int = None) -> None:
        if 0 <= idx <= 2 * MAX_ROWS:
            if value is None:
                if self._gen_tuple(self._rule_results[row_idx - 1], idx) in self._true_configs:
                    self._rule_results[row_idx][idx] = 1
                else:
                    self._rule_results[row_idx][idx] = 0
            else:
                self._rule_results[row_idx][idx] = 0

    def _gen_tuple(self, row: list, idx: int) -> tuple:
        vals = []
        if idx - 1 < 0:
            vals.append(-1)
        else:
            vals.append(row[idx - 1])

        vals.append(row[idx])

        if idx + 1 > (MAX_ROWS * 2):
            vals.append(-1)
        else:
            vals.append(row[idx + 1])

        for i in range(3):
            if vals[i] == -1:
                 vals[i] = vals[1]

        return tuple(vals)
