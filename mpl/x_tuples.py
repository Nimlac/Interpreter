class Tuple:

    @staticmethod
    def tuple_new(inter, args):
        return Tuple(inter, args)

    def __init__(self, inter, args):
        if len(args) == 0 or len(args) > 9:
            raise Exception("! Invalid args for Tp:new !")
        self.vals = []
        for arg in args:
            self.vals.append(inter.eval(arg))
        self.len = len(args)

    def item(self, inter, args):
        if len(args) < 1 or len(args) > 2  or not (arg := inter.eval(args[0]).val).is_integer() or int(arg) > self.len:
            raise Exception("! Invalid args for Tp:item !")
        if len(args) == 1:
            return self.vals[int(arg)]
        else:
            self.vals[int(arg)] = inter.eval(args[1])

    def item1(self, inter, args):
        if self.len < 1 or len(args) < 1 or len(args) > 2:
            raise Exception("! Invalid args for Tp:item !")
        if len(args) == 1:
            return self.vals[0]
        else:
            self.vals[0] = inter.eval(args[0])

    def item2(self, inter, args):
        if self.len < 2 or len(args) < 1 or len(args) > 2:
            raise Exception("! Invalid args for Tp:item !")
        if len(args) == 1:
            return self.vals[1]
        else:
            self.vals[1] = inter.eval(args[0])

    def item3(self, inter, args):
        if self.len < 3 or len(args) < 1 or len(args) > 2:
            raise Exception("! Invalid args for Tp:item !")
        if len(args) == 1:
            return self.vals[2]
        else:
            self.vals[2] = inter.eval(args[0])

    def item4(self, inter, args):
        if self.len < 4 or len(args) < 1 or len(args) > 2:
            raise Exception("! Invalid args for Tp:item !")
        if len(args) == 1:
            return self.vals[3]
        else:
            self.vals[3] = inter.eval(args[0])

    def item5(self, inter, args):
        if self.len < 5 or len(args) < 1 or len(args) > 2:
            raise Exception("! Invalid args for Tp:item !")
        if len(args) == 1:
            return self.vals[4]
        else:
            self.vals[4] = inter.eval(args[0])

    def item6(self, inter, args):
        if self.len < 6 or len(args) < 1 or len(args) > 2:
            raise Exception("! Invalid args for Tp:item !")
        if len(args) == 1:
            return self.vals[5]
        else:
            self.vals[5] = inter.eval(args[0])

    def item7(self, inter, args):
        if self.len < 7 or len(args) < 1 or len(args) > 2:
            raise Exception("! Invalid args for Tp:item !")
        if len(args) == 1:
            return self.vals[6]
        else:
            self.vals[6] = inter.eval(args[0])

    def item8(self, inter, args):
        if self.len < 8 or len(args) < 1 or len(args) > 2:
            raise Exception("! Invalid args for Tp:item !")
        if len(args) == 1:
            return self.vals[7]
        else:
            self.vals[7] = inter.eval(args[0])

    def item9(self, inter, args):
        if self.len < 9 or len(args) < 1 or len(args) > 2:
            raise Exception("! Invalid args for Tp:item !")
        if len(args) == 1:
            return self.vals[0]
        else:
            self.vals[0] = inter.eval(args[0])
