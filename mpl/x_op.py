from x_types import Bool


def op_eq(inter, args):
    if len(args) != 2:
        raise Exception("! Invalid args for equals !")
    return Bool(inter.eval(args[0]) == inter.eval(args[1]))


def op_uneq(inter, args):
    if len(args) != 2:
        raise Exception("! Invalid args for unequals !")
    return Bool(inter.eval(args[0]) != inter.eval(args[1]))


def op_gt(inter, args):
    if len(args) != 2:
        raise Exception("! Invalid args for greater than !")
    return Bool(inter.eval(args[0]) > inter.eval(args[1]))


def op_lt(inter, args):
    if len(args) != 2:
        raise Exception("! Invalid args for less than !")
    return Bool(inter.eval(args[0]) < inter.eval(args[1]))


def op_gteq(inter, args):
    if len(args) != 2:
        raise Exception("! Invalid args for greater or equal to !")
    return Bool(inter.eval(args[0]) >= inter.eval(args[1]))


def op_lteq(inter, args):
    if len(args) != 2:
        raise Exception("! Invalid args for less or equal to !")
    return Bool(inter.eval(args[0]) <= inter.eval(args[1]))
