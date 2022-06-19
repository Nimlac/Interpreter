from Environment import Env
from warnings import warn
from x_types import String


class ClassObj:
    def __init__(self, inter, class_ref, args):
        self._class = class_ref
        self.vars = class_ref.vars.copyEnv()
        self.funcs = class_ref.funcs.copyEnv()
        self._inter = inter
        if '...new' in self.funcs:
            self.funcs['...new'].run(self, args)
            # co:is(c:new())
            # co:vars(name, val) -> co.name:val()
            # co:vars(name, is, "default") -> co.name:is("default")
            # co:funcs(change_name, "New name") -> co.change_name:run("New name")   ^^

    def getclass(self):
        return String(self._class.name)

    def eval(self, text, varst=None, funcst=None):
        return self._inter.eval(text, self.vars, self.funcs, self)

    def string(self, inter, args):
        if '...string' in self.funcs:
            return self.funcs['...string'].run(self, args)
        else:
            raise Exception(f"! {self._class.name} doesn't define -> string !")

    def toNum(self, inter, args):
        if '...num' in self.funcs:
            return self.funcs['...num'].run(self, args)
        else:
            raise Exception(f"! {self._class.name} doesn't define -> num !")

    def co_old(self, inter, args):
        warn("This method is deprecated and doesn't work with variables outside of the class", DeprecationWarning, stacklevel=2)
        return self.eval(f"{args[0]}:{args[1]}({','.join(args[2:]) if len(args) > 2 else ''})")

    def co(self, inter, args):
        host = args[0]
        func = args[1]
        args = args[2:] if len(args) > 2 else ['']

        if ':' in host:
            return self.eval(f"{host}:{func}({','.join(args)})")

        if host in self.vars or host in self.funcs or func == 'is':
            if func == 'is':  # todo fixed it?
                if len(args) != 1:
                    raise Exception(f"! Invalid variable args {host}:{func}({','.join(args)}) !")
                self.vars[host] = inter.eval(args[0].strip())
            elif func == 'val':
                if args[0] != '' or len(args) != 1:
                    raise Exception(f"! Invalid variable args {host}:{func}({','.join(args)}) !")
                if host in self.vars:
                    return self.vars[host]
                else:
                    raise Exception(f"! unknown reference {host}:{func} !")
            elif func == 'run':
                if host in self.funcs:
                    return self.funcs[host].func_val_run(self, [inter.eval(arg) for arg in args] if len(args) != 1 and args[0] != '' else [])
                else:
                    raise Exception(f"! unknown reference {host}:{func} !")
            else:  # todo fixed it?
                var = self.vars[host]
                if hasattr(type(var), func):
                    return getattr(var, func)(self, [inter.eval(arg) for arg in args] if len(args) != 1 and args[0] != '' else args)
                else:
                    raise Exception(f"! {host} has no method {type(var)}:{func} !")
        elif host in inter.classes:
            if func == 'new':
                return inter.classes[host].new(inter, args)
        else:
            raise Exception(f"! unknown reference {host}:{func} !")

    def __eq__(self, other):
        if '...eq' in self.funcs:
            return self.funcs['...eq'].run(self, [other])
        else:
            raise Exception(f"! {self._class.name} doesn't define eq !")

    def __add__(self, other):
        if '...add' in self.funcs:
            return self.funcs['...add'].run(self, [other])
        else:
            raise Exception(f"! {self._class.name} doesn't define add !")

    def __sub__(self, other):
        if '...sub' in self.funcs:
            return self.funcs['...sub'].run(self, [other])
        else:
            raise Exception(f"! {self._class.name} doesn't define sub !")

    def __mul__(self, other):
        if '...mul' in self.funcs:
            return self.funcs['...mul'].run(self, [other])
        else:
            raise Exception(f"! {self._class.name} doesn't define mul !")

    def __truediv__(self, other):
        if '...div' in self.funcs:
            return self.funcs['...div'].run(self, [other])
        else:
            raise Exception(f"! {self._class.name} doesn't define div !")

    def __mod__(self, other):
        if '...mod' in self.funcs:
            return self.funcs['...mod'].run(self, [other])
        else:
            raise Exception(f"! {self._class.name} doesn't define mod !")


class Class:
    def __init__(self, inter, name, args):
        if len(args) > 2:
            raise Exception(f'! Invalid args in definition of class {name} !')
        if len(args) == 1:
            self.name = name
            self.vars = Env()
            self.funcs = Env()
            inter.evalclass(self, args[0])
        else:
            c = inter.classes[args[0]]
            self.name = name
            self.baseclass = c.new()

            self.vars = c.vars.copyEnv()
            self.vars.add_layer()

            self.funcs = c.funcs.copyEnv()
            self.funcs.add_layer()

            inter.evalclass(self, args[1])

    def new(self, inter, args):
        return ClassObj(inter, self, [inter.eval(arg) for arg in args])
