import x_sys
from x_types import String, Num, Bool, Array, Func
from x_classes import Class, ClassObj
import x_math
import x_op
import x_exp

from Environment import Env

import re


class Interpreter:

    pattern_num = re.compile(r'^-?\d+(?:\.\d+)?$')
    pattern_string = re.compile(r'^"[^():]*"$')
    pattern_bool = re.compile(r'^(?:un)?true$')

    def __init__(self):
        self.vars = Env()
        self.funcs = Env()
        self.classes = Env()
        self.libs = {
            'Sys': {
                'print': x_sys.sys_print,
                'println': x_sys.sys_println,
                'input': x_sys.sys_input
            },
            'M': {
                'add': x_math.m_add,
                'sub': x_math.m_sub,
                'mul': x_math.m_mul,
                'div': x_math.m_div,
                'pow': x_math.m_pow,
                'sqrt': x_math.m_sqrt,
                'round': x_math.m_round,
                'floor': x_math.m_floor,
                'ceil': x_math.m_ceil,
                'abs': x_math.m_abs,
                'mod': x_math.m_mod
            },
            'Op': {
                'eq': x_op.op_eq,
                'uneq': x_op.op_uneq,
                'gt': x_op.op_gt,
                'lt': x_op.op_lt,
                'gteq': x_op.op_gteq,
                'lteq': x_op.op_lteq
            },
            'B': {
                'and': Bool.b_and,
                'or': Bool.b_or,
                'all': Bool.b_all,
                'any': Bool.b_any,
                'not': Bool.b_not
            },
            'Num': {
                'from': Num.num_from,
                'maxval': Num.num_maxval,
                'minval': Num.num_minval
            },
            'S': {
                'string': String.s_string,
                'sp': String.s_sp,
                'rev': String.s_rev,
                'rp': String.s_rp,
                'fm': String.s_fm
            },
            'Exp': {
                'if': x_exp.exp_if,
                'while': x_exp.exp_while,
                'for': x_exp.exp_for
            },
            'Ar': {
                'new': Array.ar_new,
                'min': Array.ar_min,
                'max': Array.ar_max,
                'rev': Array.ar_rev,
                'map': Array.ar_map,
                'filter': Array.ar_filter
            }
        }

    def evalclass(self, classobj, text):

        text = text.replace('\n', '')
        if len(text) == 0:
            raise Exception
        text += '#'
        index = 0
        current = text[0]

        host = ''
        target = 0
        func = ''
        arg = ''
        args = []
        count = 0

        while current != '#':
            # process current
            if target == 0:
                if current == ':':
                    target = 1
                else:
                    host += current
            elif target == 1:
                if current == '(':
                    target = 2
                    count += 1
                else:
                    func += current
            else:
                if current == '(':
                    count += 1
                if current == ')':
                    count -= 1
                    if count == 0:
                        args.append(arg)
                        self.executeclasscmd(classobj, host.lstrip(), func, args)
                        host = func = arg = ''
                        target = 0
                        args = []
                    else:
                        arg += current
                else:
                    if current == ',' and count == 1:
                        args.append(arg.strip())
                        arg = ''
                    else:
                        arg += current
            index += 1
            current = text[index]

    def eval(self, text, varst=None, funcst=None, evalt=None):
        if varst is None:
            varst = self.vars
        if funcst is None:
            funcst = self.funcs

        if not (type(text) == str):
            return text

        if text == '':
            return None
        if ':' in text:
            index = 0
            current = text[0]

            text += '#'
            host = ''
            target = 0
            func = ''
            arg = ''
            args = []
            count = 0

            value = None

            while current != '#':
                # process current
                if target == 0:
                    if current == ':':
                        target = 1
                    else:
                        host += current
                elif target == 1:
                    if current == '(':
                        count += 1
                        target = 2
                    elif current == ':':
                        host += ':' + func
                        func = ''
                    else:
                        func += current
                else:
                    if current == '(':
                        count += 1
                    if current == ')':
                        count -= 1
                        if count == 0:
                            args.append(arg)
                            value = self.execute(host.lstrip() if host != '' else value, func, args, varst, funcst, evalt)
                            host = func = arg = ''
                            target = 0
                            args = []
                        else:
                            arg += current
                    else:
                        if current == ',' and count == 1:
                            args.append(arg.strip())
                            arg = ''
                        else:
                            arg += current
                index += 1
                current = text[index]
            return value
        text = text.strip()
        if Interpreter.pattern_num.match(text):
            return Num(float(text))
        elif Interpreter.pattern_string.match(text):
            return String(text[1:-1])
        elif Interpreter.pattern_bool.match(text):
            return Bool(text == 'true')
        else:
            raise Exception(f"! Invalid term {text} !")

    def interpret(self, text):
        val = None
        text = text.replace('\n', '')

        if (length := len(text)) == 0:
            return

        index = 0
        current = text[0]

        host = ''
        target = 0
        func = ''
        arg = ''
        args = []
        count = 0

        while current != '#':
            # process current
            if target == 0:
                if current == ':':
                    target = 1
                else:
                    host += current
            elif target == 1:
                if current == '(':
                    target = 2
                    count += 1
                elif current == ':':
                    host += ':' + func
                    func = ''
                else:
                    func += current
            else:
                if current == '(':
                    count += 1
                if current == ')':
                    count -= 1
                    if count == 0:
                        args.append(arg)
                        val = self.execute(host.lstrip() if host != '' else val, func, args)
                        host = func = arg = ''
                        target = 0
                        args = []
                    else:
                        arg += current
                else:
                    if current == ',' and count == 1:
                        args.append(arg.strip())
                        arg = ''
                    else:
                        arg += current
            index += 1
            if index == length:
                break
            current = text[index]

    def execute(self, host, func: str, args: [], varst=None, funcst=None, evalt=None):
        if varst is None:
            varst = self.vars

        if funcst is None:
            funcst = self.funcs

        if type(host) == str:
            if ':' in host:
                host, *extension = host.split(':')
                extension = ':'.join(extension)
                v = varst[host]
                if type(v) != ClassObj:
                    raise Exception(f"! Cannot acces variable {extension} of non Class object {host} !")
                if ':' in extension:
                    return v.eval(f"{extension}:{func}({','.join(args)})")  # todo fix args not in correct env
                else:
                    return v.co(self, [extension, func, *args])
            elif host in self.libs.keys() and func in self.libs[host].keys():
                f = self.libs[host][func]
                return f(evalt or self, args)  # todo fixit
            elif host in varst or host in funcst or func in ['func', 'is']:
                if func == 'is':
                    if len(args) != 1:
                        raise Exception(f"! Invalid variable args {host}:{func}({','.join(args)}) !")
                    arg = args[0].strip()
                    if ':' in arg:
                        varst[host] = (evalt or self).eval(arg, varst, funcst)
                    elif Interpreter.pattern_num.match(arg):
                        varst[host] = Num(float(arg))
                    elif Interpreter.pattern_string.match(arg):
                        varst[host] = String(arg[1:-1])
                    elif Interpreter.pattern_bool.match(arg):
                        varst[host] = Bool(arg == 'true')
                    else:
                        raise Exception(f"! Invalid term {arg} !")
                    return varst[host]
                elif func == 'val':
                    if args[0] != '' or len(args) != 1:
                        raise Exception(f"! Invalid variable args {host}:{func}({','.join(args)}) !")
                    if host in varst:
                        return varst[host]
                    else:
                        raise Exception(f"! unknown reference {host}:{func} !")
                elif func == 'func':
                    funcst[host] = Func(self, args)
                elif func == 'run':
                    if host in funcst:
                        return funcst[host].run(evalt or self, args)
                    else:
                        raise Exception(f"! unknown reference {host}:{func} !")
                else:
                    var = varst[host]
                    if hasattr(type(var), func):
                        return getattr(var, func)(self, args)
                    #                    elif type(var) == ClassObj:
                    #                        if True:
                    #                            pass
                    else:
                        raise Exception(f"! {host} has no method {type(var) if type(var) != ClassObj else var.getclass()}:{func} !")
            elif func == 'class':
                if host in self.classes:
                    raise Exception(f"! class already exists {host}:{func} !")
                self.classes[host] = Class(self, host, args)
            elif host in self.classes:
                if func == 'new':
                    return self.classes[host].new(self, args)
            elif self.pattern_num.match(host) or self.pattern_string.match(host) or Interpreter.pattern_bool.match(host):
                var = self.eval(host)
                if hasattr(type(var), func):
                    return getattr(var, func)(self, args)
            else:
                raise Exception(f"! unknown reference {host}:{func} !")
        else:
            if hasattr(type(host), func):
                return getattr(host, func)(self, args)
            else:
                raise Exception(f"! {host} has no method {type(host)}:{func} !")

    def executeclasscmd(self, cl, host, func, args):
        if func == 'var':
            if args[0] == '':
                cl.vars[host] = None
            elif len(args) == 1:
                cl.vars.add_var(host, self.eval(args[0]))
            else:
                raise Exception('! Invalid args for var !')
        elif func == 'func':
            if len(args) > 1:
                cl.funcs[host] = Func(self, args)
            else:
                raise Exception('! Invalid args for func !')


def main() -> None:
    with open("code.col") as file:
        text = file.read()
    i = Interpreter()
    i.interpret(text)


if __name__ == '__main__':
    main()
