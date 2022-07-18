import x_sys
from x_types import String, Num, Bool, Array, Func, Dict
from x_tuples import Tuple
from x_classes import Class, ClassObj
import x_math
import x_op
import x_exp
import x_regex

from Environment import Env

import re


class Interpreter:  # todo proper strings with escaped chars regex strings single quotes? e.g: '^-?\d+(?:\.\d+)?$' -> Num in col

    pattern_num = re.compile(r'^-?\d+(?:\.\d+)?$')
    pattern_string = re.compile(r'^".*"$|^\'.*\'$')
    pattern_bool = re.compile(r'^(?:un)?true$')
    classes = Env()

    def __init__(self):
        self.vars = Env()
        self.funcs = Env()
        self.imports = []
        self.libs = {
            'Sys': {
                'print': x_sys.sys_print,
                'println': x_sys.sys_println,
                'input': x_sys.sys_input,
                'import': x_sys.sys_import,
                'include': x_sys.sys_include,
                'hash': x_sys.sys_hash
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
                'fm': String.s_fm,
                'ascii': String.s_ascii
            },
            'Exp': {
                'if': x_exp.exp_if,
                'while': x_exp.exp_while,
                'for': x_exp.exp_for,
                'return': x_exp.exp_return,
                'break': x_exp.exp_break,
                'continue': x_exp.exp_continue
            },
            'Ar': {
                'new': Array.ar_new,
                'min': Array.ar_min,
                'max': Array.ar_max,
                'rev': Array.ar_rev,
                'map': Array.ar_map,
                'filter': Array.ar_filter
            },
            'Dict': {
                'new': Dict.dic_new
            },
            'Tuple': {
                'new': Tuple.tuple_new()
            }
        }
        
        x_sys.sys_import(self, ['"sys.col"'])

    def evallib(self, libname, text):
        if libname in self.libs:
            return
        self.libs[libname] = {}
        index = 0
        current = text[0]

        text += '#'
        host = ''
        target = 0
        func = ''
        arg = ''
        args = []
        count = 0
        quotes = False

        value = None

        while current != '#':
            # process current
            if target == 0:
                if current == ':' and not quotes:
                    target = 1
                else:
                    host += current
            elif target == 1:
                if current == '(' and not quotes:
                    count += 1
                    target = 2
                elif current == ':' and not quotes:
                    host += ':' + func
                    func = ''
                else:
                    func += current
            else:
                if current == '(' and not quotes:
                    count += 1
                if current == ')' and not quotes:
                    count -= 1
                    if count == 0:
                        args.append(arg)
                        value = self.execlibcmd(host.lstrip() if host != '' else value, func, args)
                        if len(value) == 2:
                            self.libs[libname][value[0]] = value[1]
                        host = func = arg = ''
                        target = 0
                        args = []
                    else:
                        arg += current
                else:
                    if current == ',' and count == 1 and not quotes:
                        args.append(arg.strip())
                        arg = ''
                    else:
                        arg += current
            index += 1
            current = text[index]
        return value

    def include(self, namespace):
        if namespace == 'IO':
            self.libs['IO'] = x_sys.get_IO_include()
        elif namespace == 'Regex':
            self.libs['Regex'] = x_regex.get_regex_include()
        else:
            raise Exception(f"! Unknown include {namespace} !")

    def evalclass(self, classobj, text):
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
            quotes = False

            value = None

            while current != '#':
                # process current
                if target == 0:
                    if current == ':' and not quotes:
                        target = 1
                    else:
                        host += current
                elif target == 1:
                    if current == '(' and not quotes:
                        count += 1
                        target = 2
                    elif current == ':' and not quotes:
                        host += ':' + func
                        func = ''
                    else:
                        func += current
                else:
                    if current == '(' and not quotes:
                        count += 1
                    if current == ')' and not quotes:
                        count -= 1
                        if count == 0:
                            args.append(arg)
                            value = self.execute(host.lstrip() if host != '' else value, func, args, varst, funcst, evalt)
                            if type(value) == x_exp.Exp:
                                return value
                            host = func = arg = ''
                            target = 0
                            args = []
                        else:
                            arg += current
                    else:
                        if current == ',' and count == 1 and not quotes:
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
            s = ''
            backslash = False
            quotes = 0
            for current in text:
                if backslash:
                    backslash = False
                    if quotes == 1:
                        if current == 'n':
                            s += '\n'
                        elif current == 't':
                            s += '\t'
                        elif current == '"':
                            s += '"'
                        elif current == 'r':
                            s += '\r'
                        elif current == 'b':
                            s += '\b'
                        elif current != '\\':
                            raise Exception(f"! Cannot escape character {current} !")
                    elif quotes == 2:
                        if current != "'":
                            s += f"\\{current}"
                        else:
                            s += current
                elif current == '"' and quotes != 2:  # not \
                    quotes = 1 - quotes
                elif current == "'" and quotes != 1:  # not \
                    quotes = 2 - quotes
                elif current == '\\' and quotes:
                    backslash = True
                else:
                    s += current
            return String(s)
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
        backslash = False
        quotes = False

        while current != '#':
            if target == 0:
                if current == ':' and not quotes:
                    target = 1
                else:
                    host += current
            elif target == 1:
                if current == '(' and not quotes:
                    target = 2
                    count += 1
                elif current == ':' and not quotes:
                    host += ':' + func
                    func = ''
                else:
                    func += current
            else:
                if current == '(' and not quotes:
                    count += 1
                if current == ')' and not quotes:
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
                    if current == ',' and count == 1 and not quotes:
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
                        varst[host] = (evalt or self).eval(arg, varst, funcst), evalt or self
                    elif Interpreter.pattern_num.match(arg):
                        varst[host] = Num(float(arg)), evalt or self
                    elif Interpreter.pattern_string.match(arg):
                        varst[host] = String(arg[1:-1]), evalt or self
                    elif Interpreter.pattern_bool.match(arg):
                        varst[host] = Bool(arg == 'true'), evalt or self
                    else:
                        raise Exception(f"! Invalid term {arg} !")
                    return varst[host, evalt or self]
                elif func == 'val':
                    if args[0] != '' or len(args) != 1:
                        raise Exception(f"! Invalid variable args {host}:{func}({','.join(args)}) !")
                    if host in varst:
                        return varst[host, evalt or self]
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
                if host in Interpreter.classes:
                    raise Exception(f"! class already exists {host}:{func} !")
                Interpreter.classes[host] = Class(self, host, args)
            elif func == 'lib':
                if len(args) != 1:
                    raise Exception
                self.evallib(host, args[0])
            elif host in Interpreter.classes:
                if func == 'new':
                    return Interpreter.classes[host].new(self, args)
            elif self.pattern_num.match(host) or self.pattern_string.match(host) or Interpreter.pattern_bool.match(host):
                var = self.eval(host)
                if hasattr(type(var), func):
                    return getattr(var, func)(self, args)
            else:
                raise Exception(f"! unknown reference {host}:{func} !")
        else:
            if type(host) == ClassObj:
                host.co(self, [host.class_ref.name, func, args])
            elif hasattr(type(host), func):
                return getattr(host, func)(self, args)
            else:
                raise Exception(f"! {host} has no method {type(host)}:{func} !")

    def execlibcmd(self, host, func, args):
        if func == 'class':
            self.execute(host, func, args)
            return [False]
        elif func == 'func':
            if len(args) > 1:
                return [host, Func(self, args)]
            else:
                raise Exception('! Invalid args for func !')
        raise Exception

    def executeclasscmd(self, cl, host, func, args):
        if func == 'var':
            if args[0] == '':
                cl.vars[host] = None
            elif len(args) == 1:
                cl.vars.add_var(host, self.eval(args[0]))
            else:
                raise Exception('! Invalid args for var !')
        elif func == 'pvar':
            if args[0] == '':
                cl.vars[host] = [None]
            elif len(args) == 1:
                cl.vars.add_var(host, [self.eval(args[0])])
            else:
                raise Exception('! Invalid args for pvar !')
        elif func == 'func':
            if len(args) > 1:
                cl.funcs[host] = Func(self, args)
            else:
                raise Exception('! Invalid args for func !')
        elif func == 'pfunc':
            if len(args) > 1:
                cl.funcs[host] = Func(self, args, private=True, cl=cl)
            else:
                raise Exception('! Invalid args for pfunc !')


def main() -> None:
    with open("code.col") as file:
        text = file.read()
    i = Interpreter()
    i.interpret(text)


if __name__ == '__main__':
    main()
