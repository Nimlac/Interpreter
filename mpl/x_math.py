from x_types import Num
import math


def m_add(inter, args):
    if len(args) == 1:
        raise Exception("! Invalid args for add !")
    val = inter.eval(args[0])
    for arg in args[1:]:
        val += inter.eval(arg)
    return val


def m_sub(inter, args):
    if len(args) == 1:
        raise Exception("! Invalid args for sub !")
    val = inter.eval(args[0])
    for arg in args[1:]:
        val -= inter.eval(arg)
    return val


def m_mul(inter, args):
    if len(args) == 1:
        raise Exception("! Invalid args for mul !")
    val = inter.eval(args[0])
    for arg in args[1:]:
        val *= inter.eval(arg)
    return val


def m_div(inter, args):
    if len(args) == 1:
        raise Exception("! Invalid args for add !")
    val = inter.eval(args[0])
    for arg in args[1:]:
        val /= inter.eval(arg)
    return val


def m_pow(inter, args):
    if len(args) != 2:
        raise Exception("! Invalid args for pow !")
    return inter.eval(args[0]) ** inter.eval(args[1])


def m_sqrt(inter, args):
    if len(args) > 2:
        raise Exception("! Invalid args for sqrt !")
    return m_pow(inter, [inter.eval(args[0]), Num(1)/inter.eval(args[1]) if len(args) == 2 else Num(0.5)])


def m_round(inter, args):
    if len(args) != 1:
        raise Exception("! Invalid args for round !")
    return Num(round(inter.eval(args[0]).val))


def m_floor(inter, args):
    if len(args) != 1:
        raise Exception("! Invalid args for floor !")
    return Num(math.floor(inter.eval(args[0]).val))


def m_ceil(inter, args):
    if len(args) != 1:
        raise Exception("! Invalid args for ceil !")
    return Num(math.ceil(inter.eval(args[0]).val))


def m_abs(inter, args):
    if len(args) != 1:
        raise Exception("! Invalid args for abs !")
    return Num(abs(inter.eval(args[0]).val))


def m_mod(inter, args):
    if len(args) != 2:
        raise Exception("! Invalid args for mod !")
    return inter.eval(args[0]) % inter.eval(args[1])
