class Exp:
    def __init__(self, etype, value=None):
        self.etype = etype
        self.value = value


def exp_if(inter, args):
    if len(args) > 3 or len(args) < 2:
        raise Exception("! Invalid args for Exp:if !")
    if inter.eval(args[0]):
        return inter.eval(args[1])
    elif len(args) == 3:
        return inter.eval(args[2])
    else:
        return None


def exp_while(inter, args):
    if len(args) != 2:
        raise Exception("! Invalid args for Exp:while !")
    val = None

    while inter.eval(args[0]):
        val = inter.eval(args[1])
        if type(val) == Exp:
            if val.etype == 0:
                return None
            elif val.etype == 1:
                val = None
    return val


def exp_for(inter, args):
    if len(args) == 4:
        val = None
        inter.vars.add_layer()
        inter.eval(args[0])
        while inter.eval(args[1]):
            val = inter.eval(args[3])
            inter.eval(args[2])
        inter.vars.rem_layer()
        return val
    elif len(args) == 3:  # Exp:for(c,s, *code*)  / for c in s: *code*
        val = None
        inter.vars.add_layer()
        inter.vars.add_var(name := args[0], None)
        for v in inter.eval(args[1]).array(None, ['']).val:
            inter.vars[name] = v
            val = inter.eval(args[2])
            if type(val) == Exp:
                if val.etype == 0:
                    return None
                elif val.etype == 1:
                    val = None
        inter.vars.rem_layer()
        return val
    else:
        raise Exception("! Invalid args for Exp:for !")


def exp_return(inter, args):
    if len(args) != 1:
        raise Exception("! Invalid args for Exp:return !")
    return Exp(-1, inter.eval(args[0]))


def exp_break(inter, args):
    if len(args) != 1:
        raise Exception("! Invalid args for Exp:break !")
    return Exp(0) if args[0] != '' == bool(inter.eval(args[0])) else None


def exp_continue(inter, args):
    if len(args) != 1:
        raise Exception("! Invalid args for Exp:continue !")
    return Exp(1) if args[0] != '' == bool(inter.eval(args[0])) else None


