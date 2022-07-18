from x_types import String, Bool, Array
from os.path import exists


def sys_print(inter, args):
    if len(args) != 1:
        raise Exception("! Invalid args for print !")
    print(inter.eval(args[0]).string(inter, args), end='')


def sys_println(inter, args):
    if len(args) != 1:
        raise Exception("! Invalid args for println !")
    print(inter.eval(args[0]).string(inter, args))


def sys_input(inter, args) -> String:
    if len(args) != 1:
        raise Exception("! Invalid args for input !")
    if len(args) == 1 and args[0] == '':
        return String(input())
    else:
        return String(input(inter.eval(args[0]).string(inter, args)))


def sys_import(inter, args):
    if len(args) > 1 or args[0] == '' or type(var := inter.eval(args[0])) != String:
        raise Exception("! Invalid args for import !")
    if exists(var.val):
        if var.val in inter.imports:
            return
        inter.imports.append(var.val)
        with open(var.val) as f:
            inter.eval(f.read())
    else:
        raise Exception(f"! File {var.val} doesn't exist !")


def sys_read(inter, args):
    if len(args) != 3:
        raise Exception("! Invalid args for read !")
    if exists(filename := inter.eval(args[1]).val):
        reader = Reader(filename)
        inter.vars[args[0]] = reader
        inter.eval(args[2])
        reader.close(inter, [''])
    else:
        raise Exception(f"! File {filename} doesn't exist !")


def sys_write(inter, args):
    if not(2 < len(args) < 5):
        raise Exception("! Invalid args for write !")
    if exists(filename := inter.eval(args[1]).val):
        writer = Writer(filename, args[2] if len(args) == 4 else False)
        inter.vars[args[0]] = writer
        inter.eval(args[-1])
        writer.close(inter, [''])
    else:
        raise Exception(f"! File {filename} doesn't exist !")


def sys_writer(inter, args):
    if len(args) > 2:
        raise Exception("! Invalid args for read !")
    if exists(filename := inter.eval(args[0]).val):
        return Writer(filename, args[1] if len(args) == 2 else False)
    else:
        raise Exception(f"! File {filename} doesn't exist !")


def sys_reader(inter, args):
    if len(args) != 1:
        raise Exception("! Invalid args for read !")
    if exists(filename := inter.eval(args[0]).val):
        return Reader(filename)
    else:
        raise Exception(f"! File {filename} doesn't exist !")


def sys_hash(inter, args):
    if len(args) != 1 or args[0] != '':
        raise Exception("! Invalid args for read !")
    return hash([inter.eval(x) for x in args])


def sys_include(inter, args):
    if len(args) == 0 and args[0] == '':
        raise Exception("! Invalid args for Sys:include !")
    for arg in args:
        inter.include(arg)


def get_IO_include():
    return {
        'read': sys_read,
        'reader': sys_reader,
        'write': sys_write,
        'writer': sys_writer,
    }


class Writer:
    def __init__(self, filename, append):
        self.file = open(filename, 'a' if append else 'w')
        self.id = hash(self)

    def write(self, inter, args):
        self.writeline(inter, args, False)

    def writeline(self, inter, args, newline=True):
        if len(args) != 1:
            raise Exception("! Invalid args for Writer:writeline !")
        self.file.write(inter.eval(args[0]).string(inter, [''])+('\n'if newline else ''))

    def close(self, inter, args):
        if len(args) != 1 or args[0] != '':
            raise Exception("! Invalid args for Writer:close !")
        self.file.close()
        inter.vars.remvar(type(self), self.id)


class Reader:
    def __init__(self, filename):
        self.file = open(filename, 'r')
        self._next = -1
        self.id = hash(self)

    def readall(self, inter, args) -> Array:
        if len(args) != 1 or args[0] != '':
            raise Exception("! Invalid args for Reader:readall !")
        return Array([String(x) for x in self.file.read().split('\n')])

    def readline(self, inter, args) -> String:
        if len(args) != 1 or args[0] != '':
            raise Exception("! Invalid args for Reader:readline !")
        if self._next == -1:
            return String(self.file.readline().replace('\n', ''))
        line = self._next
        self._next = -1
        return String(line.replace('\n', ''))

    def done(self, inter, args) -> Bool:
        if len(args) != 1 or args[0] != '':
            raise Exception("! Invalid args for Reader:done !")
        if self._next == -1:
            self._next = self.file.readline()
        return Bool(self._next == '')

    def close(self, inter, args):
        if len(args) != 1 or args[0] != '':
            raise Exception("! Invalid args for Reader:close !")
        self.file.close()
        inter.vars.remvar(type(self), self.id)
