def exp_if(inter, args):
    if len(args) > 3 or len(args) < 2:
        raise Exception("! Invalid args for if-condition !")
    if inter.eval(args[0]):
        return inter.eval(args[1])
    elif len(args) == 3:
        return inter.eval(args[2])
    else:
        return None


def exp_while(inter, args):
    if len(args) != 2:
        raise Exception("! Invalid args for while-loop !")
    val = None

    while inter.eval(args[0]):
        val = inter.eval(args[1])
    return val


def exp_for(inter, args):
    if len(args) != 4:
        raise Exception("! Invalid args for for-loop !")
    val = None
    inter.eval(args[0])
    while inter.eval(args[1]):
        val = inter.eval(args[3])
        inter.eval(args[2])
    return val

