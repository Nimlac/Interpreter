from copy import deepcopy


class Env:
    def __init__(self, colval=None, cl=None):
        self.col = colval or [{}]
        self.cl = cl

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

    def __getitem__(self, item, cl=None):
        if type(item) == tuple:
            cl = item[1].class_ref.name if hasattr(item[1], 'class_ref') else None
            item = item[0]
        for i in range(len(self.col)+1):
            if item in self.col[-i]:
                if type(var := self.col[-i][item]) == list:
                    if self.cl != cl or cl is None:
                        raise Exception(f"! Cannot access private atribute {item} !")
                    return var[0]
                else:
                    return var
        return None

    def __setitem__(self, key, value, cl=None):
        if type(value) == tuple:
            cl = value[1].class_ref.name if hasattr(value[1], 'class_ref') else None
            value = value[0]
        flag = True
        for i in range(len(self.col)+1):
            if key in self.col[-i]:
                if type(self.col[-i][key]) == list:
                    if self.cl != cl or cl is None:
                        raise Exception(f"! Cannot access private atribute {key} !")
                    self.col[-i][key] = [value]
                else:
                    self.col[-i][key] = value
                flag = False
        if flag:
            self.add_var(key, value)

    def debug_log(self):
        return ': :'.join('-'.join(c) for c in self.col)

    def add_var(self, key, value):
        self.col[-1][key] = value

    def copyEnv(self):
        return Env(deepcopy(self.col), cl=self.cl)

    def remvar(self, ty, _id):
        for i in range(len(self.col)+1):
            if len(y := [(k, x) for k, x in self.col[-i].items() if type(x) == ty]):
                del self.col[-i][[k for k, o in y if o.id == _id][0]]

