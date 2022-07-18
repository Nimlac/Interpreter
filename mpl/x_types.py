import copy
import sys
from x_exp import Exp


class String:
    def __init__(self, n):
        if type(n) == float:
            self._val = str(n)
        elif type(n) != str:
            self._val = str(n)
        else:
            self.val = n

    def __hash__(self):
        return hash(self.val)

    def array(self, inter, args):
        return Array([String(c) for c in self.val])

    @property
    def val(self) -> str:
        return self._val

    @val.setter
    def val(self, n: str):
        self._val = n

    @staticmethod
    def s_string(inter, args):
        if len(args) != 1:
            raise Exception("! Invalid args for String:string !")
        return inter.eval(args[0]).string(inter, args)

    @staticmethod
    def s_fm(inter, args):
        if len(args) == 1:
            raise Exception("! Invalid args for String:format !")
        s = inter.eval(args[0])
        for i in range(1, len(args)):
            x = inter.eval(args[i])
            s = String.s_rp(inter, [s, String("%"+str(i)), x.string(inter, ['']) if type(x) != String else x])
        return s

    @staticmethod
    def s_ascii(inter, args):
        if len(args) != 1:
            raise Exception("! Invalid args for String:ascii !")
        var = inter.eval(args[0])
        if type(var) == Num:
            if var.val.is_integer():
                return String(chr(int(var.val)))
            else:
                raise Exception("! Invalid args for String:ascii !")
        elif type(var) == String:
            if len(var.val) != 1:
                raise Exception("! Invalid args for String:ascii !")
            return Num(ord(var.val))
        else:
            raise Exception("! Invalid args for String:ascii !")

    @staticmethod
    def s_sp(inter, args):
        if len(args) == 1 and args[0] == '':
            raise Exception("! Invalid args for String:sp !")
        var = inter.eval(args[0])
        return Array([String(inter.eval(x).string()) for x in
                      (str(var).split() if len(args) == 1 else str(var).split(str(inter.eval(args[1]).string(inter, ['']))))])

    @staticmethod
    def s_rp(inter, args):
        if len(args) != 3:
            raise Exception("! Invalid args for String:rp !")
        return String(inter.eval(args[0]).val.replace(inter.eval(args[1]).val, inter.eval(args[2]).val))

    @staticmethod
    def s_rev(inter, args):
        if len(args) != 1:
            raise Exception("! Invalid args for String:rev !")
        return String(inter.eval(args[0]).val[::-1])

    def __str__(self):
        return self.val

    def string(self, inter, args):
        return self

    def fm(self, inter, args):
        if len(args) == 1 and args[0] == '':
            raise Exception("! Invalid args for String:format !")
        s = self
        for i in range(len(args)):
            x = inter.eval(args[i])
            s = String.s_rp(inter, [s, String("%"+str(i+1)), x.string(inter, ['']) if type(x) != String else x])
        return s

    def __contains__(self, item):
        return item.val in self.val

    def __eq__(self, other):
        return Bool(self.val == other.val)

    def __add__(self, other):
        return String(self.val + other.val)

    def __gt__(self, other):
        return Bool(self.val > other.val)

    def __ge__(self, other):
        return Bool(self.val >= other.val)

    def sp(self, inter, args):
        if len(args) != 1:
            raise Exception("! Invalid args for String:sp !")
        return Array([inter.eval(f'"{x}"') for x in
                      (str(self).split() if args[0] == '' else str(self).split(str(inter.eval(args[0]).string(inter, ['']))))])

    def rp(self, inter, args):
        if len(args) != 2:
            raise Exception("! Invalid args for String:sp !")
        self.val = self.val.replace(inter.eval(args[0]).val, inter.eval(args[1]).val)
        return self

    def get(self, inter, args):
        if len(args) != 1 or not (arg := inter.eval(args[0]).val).is_integer():
            raise Exception("! Invalid args for String:get !")
        return String(self.val[int(arg)])

    def rev(self, inter, args):
        if len(args) != 1 or args[0] != '':
            raise Exception("! Invalid args for String:rev !")
        return String(self.val[::-1])

    def toNum(self, inter, args):
        if len(args) != 1 or args[0] != '':
            raise Exception("! Invalid args for String:toNum !")
        return Num(float(self.val))

    def len(self, inter, args):
        if args[0] != '' or len(args) != 1:
            raise Exception("! Invalid args for String:len !")
        return Num(len(self.val))

    def has(self, inter, args):
        if len(args) != 1:
            raise Exception("! Invalid args for String:has !")
        return Bool(inter.eval(args[0]) in self)

    def sub(self, inter, args):
        if len(args) != 2 or not (x := (inter.eval(args[0]) or Num(0)).val).is_integer() or not (y := (inter.eval(args[1]) or Num(len(self.val))).val).is_integer():
            raise Exception("! Invalid args for String:sub !")
        return String(self.val[int(x):int(y)])

    def startswith(self, inter, args):
        if len(args) != 1:
            raise Exception("! Invalid args for String:startswith !")
        return Bool(self.val.startswith(inter.eval(args[0]).val))

    def endswith(self, inter, args):
        if len(args) != 1:
            raise Exception("! Invalid args for String:endswith !")
        return Bool(self.val.endswith(inter.eval(args[0]).val))

    def strip(self, inter, args):
        if len(args) != 1:
            raise Exception("! Invalid args for String:strip !")
        if args[0] == '':
            return String(self.val.strip(' '))
        else:
            return String(self.val.strip(inter.eval(args[0]).val))

    def lstrip(self, inter, args):
        if len(args) != 1:
            raise Exception("! Invalid args for String:lstrip !")
        if args[0] == '':
            return String(self.val.lstrip(' '))
        else:
            return String(self.val.lstrip(inter.eval(args[0]).val))

    def rstrip(self, inter, args):
        if len(args) != 1:
            raise Exception("! Invalid args for String:rstrip !")
        if args[0] == '':
            return String(self.val.rstrip(' '))
        else:
            return String(self.val.rstrip(inter.eval(args[0]).val))

    def to_char_array(self, inter, args):
        if args[0] != '' or len(args) != 1:
            raise Exception("! Invalid args for String:to_char_array !")
        return Array([String(c) for c in self.val])


class Num:
    def __init__(self, n):
        self._val = float(n)

    def __hash__(self):
        return hash(self.val)

    def inc(self, inter, args):
        if len(args) != 1:
            raise Exception("! Invalid args for Num:inc !")
        elif args[0] != '':
            self.val += inter.eval(args[0]).val
        else:
            self.val += 1
        return self

    def dec(self, inter, args):
        if len(args) != 1:
            raise Exception("! Invalid args for Num:dec !")
        elif args[0] != '':
            self.val -= inter.eval(args[0]).val
        else:
            self.val -= 1
        return self

    def mul(self, inter, args):
        if len(args) != 1:
            raise Exception("! Invalid args for Num:dec !")
        else:
            self.val *= inter.eval(args[0]).val
        return self

    def div(self, inter, args):
        if len(args) != 1:
            raise Exception("! Invalid args for Num:dec !")
        else:
            self.val /= inter.eval(args[0]).val
        return self

    @property
    def val(self) -> float:
        return self._val

    @val.setter
    def val(self, n: float):
        self._val = n

    def string(self, inter, args) -> String:
        return String(self.val)

    @staticmethod
    def num_from(inter, args):
        if len(args) != 1:
            raise Exception("! Invalid args for Num:from !")
        var = inter.eval(args[0])
        if type(var) == Num:
            return var
        return var.toNum(inter, [''])

    @staticmethod
    def num_maxval(inter, args):
        if len(args) != 1:
            raise Exception("! Invalid args for Num:maxval !")
        return Num(sys.float_info.max)

    @staticmethod
    def num_minval(inter, args):
        if len(args) != 1:
            raise Exception("! Invalid args for Num:minval !")
        return Num(sys.float_info.min)

    def __add__(self, other):
        return Num(self.val + other.val)

    def __sub__(self, other):
        return Num(self.val - other.val)

    def __truediv__(self, other):
        return Num(self.val / other.val)

    def __mod__(self, other):
        return Num(self.val % other.val)

    def __mul__(self, other):
        return Num(self.val * other.val)

    def __pow__(self, power, modulo=None):
        return Num(self.val ** power.val)

    def __eq__(self, other):
        return Bool(self.val == other.val)

    def __gt__(self, other):
        return Bool(self.val > other.val)

    def __ge__(self, other):
        return Bool(self.val >= other.val)


class Bool:
    def __init__(self, b: bool):
        self._val = b

    def __hash__(self):
        return hash(self.val)

    @property
    def val(self) -> bool:
        return self._val

    @val.setter
    def val(self, n: str):
        self._val = n

    def __bool__(self):
        return bool(self.val)

    def string(self, inter, args):
        return String('true' if self else 'untrue')

    @staticmethod
    def b_not(inter, args):
        if len(args) != 1:
            raise Exception("! Invalid args for not !")
        return Bool(not inter.eval(args[0]))

    @staticmethod
    def b_and(inter, args):
        if len(args) != 2:
            raise Exception("! Invalid args for and !")
        return Bool(inter.eval(args[0]) and inter.eval(args[1]))

    @staticmethod
    def b_or(inter, args):
        if len(args) != 2:
            raise Exception("! Invalid args for or !")
        return Bool(inter.eval(args[0]) or inter.eval(args[1]))

    @staticmethod
    def b_all(inter, args):
        if len(args) < 2:
            raise Exception("! Invalid args for all !")
        return Bool(all(inter.eval(arg) for arg in args))

    @staticmethod
    def b_any(inter, args):
        if len(args) < 2:
            raise Exception("! Invalid args for all !")
        return Bool(any(inter.eval(arg) for arg in args))


class Array:
    def __init__(self, args=None):
        if args is None or len(args) == 0:
            self._val = []
        else:
            self._val = args

    def __hash__(self):
        return hash(self.val)

    def array(self, inter, args):
        if len(args) != 1 or args[0] != '':
            raise Exception("! Invalid args for array !")
        return self

    @property
    def val(self):
        return self._val

    @val.setter
    def val(self, value):
        self._val = value

    @staticmethod
    def ar_new(inter, args):
        return Array([inter.eval(arg) for arg in args if arg != ''])

    @staticmethod
    def ar_min(inter, args):
        return min(inter.eval(arg) for arg in args)

    @staticmethod
    def ar_max(inter, args):
        return max(inter.eval(arg) for arg in args)

    @staticmethod
    def ar_rev(inter, args):
        if len(args) != 1 or type(arg := inter.eval(args[0])) != Array:
            raise Exception("! Invalid args for Array:rev !")
        return arg.rev()

    @staticmethod
    def ar_map(inter, args):
        if len(args) > 2:
            ar = inter.eval(args[0])
            if type(ar) != Array:
                raise Exception("! Invalid args for Array:map !")
            inter.vars.add_layer()
            inter.funcs.add_layer()
            f = Func(inter, args[1:])
            ar = Array([f.func_val_run(inter, ([item] if type(item) != list else item)) for item in ar.val])
            inter.vars.rem_layer()
            inter.funcs.rem_layer()
            return ar
        else:
            raise Exception("! Invalid args for Array:map !")

    @staticmethod
    def ar_filter(inter, args):
        if len(args) > 2:
            inter.vars.add_layer()
            inter.funcs.add_layer()
            ar = inter.eval(args[0])
            if type(ar) != Array:
                raise Exception("! Invalid args for Array:filter !")
            f = Func(inter, args[1:])
            ar = Array([item for item in ar.val if f.func_val_run(inter, ([item] if type(item) != list else item))])
            inter.vars.rem_layer()
            inter.funcs.rem_layer()
            return ar
        else:
            raise Exception("! Invalid args for Array:filter !")

    @staticmethod
    def ar_sort(inter, args):
        if len(args) > 2:
            inter.vars.add_layer()
            inter.funcs.add_layer()
            ar = args[0]
            if type(ar) != Array:
                raise Exception("! Invalid args for Array:map !")
            f = Func(inter, args)
            ar = sorted(ar.val, key=lambda x: f.func_val_run(inter, x))
            inter.vars.rem_layer()
            inter.funcs.rem_layer()
            return Array(ar)
        elif args[0] == '' or type(ar := inter.eval(args[0])) != Array:
            raise Exception("! Invalid args for Array:sort !")
        return Array(sorted(ar.val))

    def string(self, inter, args) -> String:
        return String('<' + '; '.join(str(item.string(inter, [''])) for item in self.val) + '>')

    def add(self, inter, args):
        if args[0] == '' and len(args) == 1:
            raise Exception("! Invalid args for Array:add !")
        self.val.append(copy.deepcopy(inter.eval(args[0])))
        return self

    def add_ref(self, inter, args):
        if args[0] == '' and len(args) == 1:
            raise Exception("! Invalid args for Array:add !")
        self.val.append(inter.eval(args[0]))
        return self

    def rem(self, inter, args):
        if args[0] == '' and len(args) == 1:
            raise Exception("! Invalid args for Array:rem !")
        for arg in args:
            self.val.remove(inter.eval(arg))
        return self

    def get(self, inter, args):
        if len(args) != 1 or not (arg := inter.eval(args[0]).val).is_integer():
            raise Exception("! Invalid args for Array:get !")
        return self.val[int(arg)]

    def set(self, inter, args):
        if len(args) != 2 or not (arg := inter.eval(args[0]).val).is_integer():
            raise Exception("! Invalid args for Array:set !")
        self.val[int(arg)] = inter.eval(args[1])
        return self

    def len(self, inter, args):
        if args[0] != '' or len(args) != 1:
            raise Exception("! Invalid args for Array:len !")
        return Num(len(self.val))

    def has(self, inter, args):
        if len(args) != 1:
            raise Exception("! Invalid args for Array:has !")
        return Bool(inter.eval(args[0]) in self.val)

    def join(self, inter, args):
        if len(args) != 1:
            raise Exception("! Invalid args for Array:join !")
        return String(f'{str(inter.eval(args[0]).string(inter, [""])).join(str(x.string(inter, [""])) for x in self.val)}')

    def map(self, inter, args):
        if len(args) > 1:
            inter.vars.add_layer()
            inter.funcs.add_layer()
            f = Func(inter, args)
            self.val = [f.func_val_run(inter, ([item] if type(item) != list else item)) for item in self.val]
            inter.vars.rem_layer()
            inter.funcs.rem_layer()
            return self
        else:
            raise Exception("! Invalid args for Array:map !")

    def filter(self, inter, args):
        if len(args) > 1:
            inter.vars.add_layer()
            inter.funcs.add_layer()
            f = Func(inter, args)
            self.val = [item for item in self.val if f.func_val_run(inter, ([item] if type(item) != list else item))]
            inter.vars.rem_layer()
            inter.funcs.rem_layer()
            return self
        else:
            raise Exception("! Invalid args for Array:filter !")

    def all(self, inter, args):
        if len(args) > 1:
            inter.vars.add_layer()
            inter.funcs.add_layer()
            f = Func(inter, args)
            val = Bool(all(f.func_val_run(inter, ([item] if type(item) != list else item)) for item in self.val))
            inter.vars.rem_layer()
            inter.funcs.rem_layer()
            return val
        else:
            return Bool(all(self.val))

    def any(self, inter, args):
        if len(args) > 1:
            inter.vars.add_layer()
            inter.funcs.add_layer()
            f = Func(inter, args)
            val = Bool(any(f.func_val_run(inter, ([item] if type(item) != list else item)) for item in self.val))
            inter.vars.rem_layer()
            inter.funcs.rem_layer()
            return val
        else:
            return Bool(any(self.val))

    def min(self, inter, args):
        if len(args) > 1:
            inter.vars.add_layer()
            inter.funcs.add_layer()
            f = Func(inter, args)
            v = min(item for item in self.val if f.func_val_run(inter, ([item] if type(item) != list else item)))
            inter.vars.rem_layer()
            inter.funcs.rem_layer()
            return v
        elif len(args) == 1 and args[0] == '':
            return min(self.val)
        else:
            raise Exception("! Invalid args for Array:min !")

    def max(self, inter, args):
        if len(args) > 1:
            inter.vars.add_layer()
            inter.funcs.add_layer()
            f = Func(inter, args)
            v = max(item for item in self.val if f.func_val_run(inter, ([item] if type(item) != list else item)))
            inter.vars.rem_layer()
            inter.funcs.rem_layer()
            return v
        elif len(args) == 1 and args[0] == '':
            return max(self.val)
        else:
            raise Exception("! Invalid args for Array:max !")

    def sum(self, inter, args):
        if len(args) > 1:
            inter.vars.add_layer()
            inter.funcs.add_layer()
            f = Func(inter, args)
            ar = [item for item in self.val if f.func_val_run(inter, ([item] if type(item) != list else item))]
            inter.vars.rem_layer()
            inter.funcs.rem_layer()
            if len(ar) == 1:
                return ar[0]
            else:
                val = ar[0]
                for i in ar[1:]:
                    val = inter.eval(f"M:add({val.val},{i.val})")
                return val
        else:
            val = self.val[0]
            for i in self.val[1:]:
                val = inter.eval(f"M:add({val.val},{i.val})")
            return val

    def rev(self, inter, args):
        if len(args) != 1 or args[0] != '':
            raise Exception("! Invalid args for Array:rev !")
        return Array(self.val[::-1])

    def sort(self, inter, args):
        if len(args) > 1:
            inter.vars.add_layer()
            inter.funcs.add_layer()
            f = Func(inter, args)
            self.val = sorted(self.val, key=lambda x: f.func_val_run(inter, x))
            inter.vars.rem_layer()
            inter.funcs.rem_layer()
        elif args[0] != '':
            raise Exception("! Invalid args for Array:sort !")
        self.val = sorted(self.val)
        return self


class Dict:
    def __init__(self):
        self.val = {}

    def __hash__(self):
        return hash(self.val)

    @staticmethod
    def dic_new(inter, args):
        if len(args) != 1 or args[0] != '':
            raise Exception("! Invalid args for Dictionary:new !")
        return Dict()

    def get(self, inter, args):  # a:get(key)
        return self.val[inter.eval(args[0])]

    def set(self, inter, args):  # a:set(key, value)
        if len(args) != 2:
            raise Exception("! Invalid args for Dictionary:set !")
        self.val[inter.eval(args[0])] = inter.eval(args[1])

    def has(self, inter, args) -> Bool:  # a:has(key) -> Bool
        if len(args) != 1:
            raise Exception("! Invalid args for Dictionary:has !")
        return Bool(inter.eval(args[0]) in self.val)

    def array(self, inter, args) -> Array:  # a:array() -> Array
        if len(args) != 1 or args[0] != '':
            raise Exception("! Invalid args for Dictionary:array !")
        # todo funcs </>
        return Array([inter.classes["ValuePair"].new(inter, [k, v]) for k, v in self.val.items()])

    def string(self, inter, agrs) -> String:
        if len(self.val) != 0:
            return String('<{(' + '), ('.join([f"{k.string(inter, [''])} -> {v.string(inter, [''])}" for k, v in self.val.items()]) + ')}>')
        return String('<{}>')


class Func:
    def __init__(self, inter, args, private=False, cl=None):
        self.names = args[:-1] if len(args) != 1 and args[0] != '' else []
        self.code = args[-1]
        self.private = private
        self.cl = cl

    def __call__(self, *args, **kwargs):
        return self.run(args[0], args[1])

    def run(self, inter, args):
        if self.private and (not hasattr(inter, 'class_ref') or inter.class_ref.name != self.cl.name):
            raise Exception(f"! Cannot access private method of class {self.cl.name}!")

        if len(args) != len(self.names) and args[0] != '':
            raise Exception("! Invalid args for run !")
        inter.vars.add_layer()
        inter.funcs.add_layer()
        for i in range(len(self.names)):
            inter.vars.add_var(str(self.names[i]), inter.eval(args[i]))
        val = inter.eval(self.code)
        if type(val) == Exp and val.etype == -1:
            val = val.value
        inter.vars.rem_layer()
        inter.funcs.rem_layer()
        return val

    def func_val_run(self, inter, args):
        if len(args) != len(self.names):
            raise Exception("! Invalid args for run !")
        inter.vars.add_layer()
        inter.funcs.add_layer()
        for i in range(len(self.names)):
            inter.vars.add_var(str(self.names[i]), args[i])
        val = inter.eval(self.code)
        if type(val) == Exp and val.etype == -1:
            val = val.value
        inter.vars.rem_layer()
        inter.funcs.rem_layer()
        return val


import main
