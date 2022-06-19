from copy import deepcopy


class Env:
    def __init__(self, colval=None):
        self.col = colval or [{}]

    def add_layer(self):
        self.col.append({})

    def rem_layer(self):
        self.col = self.col[:-1]

    def save(self, name, val):
        self.col[-1][name] = val

    def __contains__(self, item) -> bool:
        for i in range(len(self.col)+1):
            if item in self.col[-i]:
                return True
        return False

    def __getitem__(self, item):
        for i in range(len(self.col)+1):
            if item in self.col[-i]:
                return self.col[-i][item]
        return None

    def __setitem__(self, key, value):
        flag = True
        for i in range(len(self.col)+1):
            if key in self.col[-i]:
                self.col[-i][key] = value
                flag = False
        if flag:
            self.add_var(key, value)

    def debug_log(self):
        return ': :'.join('-'.join(c) for c in self.col)

    def add_var(self, key, value):
        self.col[-1][key] = value

    def copyEnv(self):
        return Env(deepcopy(self.col))
