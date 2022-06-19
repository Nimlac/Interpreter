from x_types import String


def sys_print(inter, args):
    if len(args) != 1:
        raise Exception("! Invalid args for print !")
    print(inter.eval(args[0]).string(inter, args), end='')


def sys_println(inter, args):
    if len(args) != 1:
        raise Exception("! Invalid args for println !")
    print(inter.eval(args[0]).string(inter, args))


def sys_input(inter, args) -> String:
    if len(args) > 1:
        raise Exception("! Invalid args for input !")
    if len(args) == 1 and args[0] == '':
        return String(input())
    else:
        return String(input(inter.eval(args[0]).string(inter, args)))
