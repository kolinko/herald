# basic code for printing console colors.
# usage:
# print(C.red('hello ')+C.green('world'))

class C():
    cheader = '\033[95m'
    cblue = '\033[94m'
    cokgreen = '\033[92m'
    cwarning = '\033[93m'
    cred = '\033[91m'
    cbold = '\033[1m'
    cunderline = '\033[4m'
    cgreen = '\033[32m'
    cgray = '\033[38;5;8m'
    endc = '\033[0m'
    cfail = '\033[91m'

    cgreen_back = '\033[42;1m\033[38;5;0m'
    cblue_back = '\033[43;1m\033[38;5;0m'

    every = set([cheader, cblue, cokgreen, cwarning, cred, cbold, cunderline, cgreen, cgray, endc])

    @staticmethod
    def color(exp, _color, add_color=True, color_false=None):
        if add_color:
            if exp == "":
                return ''

            return _color + exp + C.endc
        else:
            if color_false is None:
                return str(exp)
            else:
                return C.color(exp, color_false)

    @staticmethod
    def red(text, add_color=True):
        return C.color(text, C.cred, add_color)

    @staticmethod
    def blue(text, add_color=True):
        return C.color(text, C.cblue, add_color)

    @staticmethod
    def green(text, add_color=True):
        return C.color(text, C.cgreen, add_color)

    @staticmethod
    def okgreen(text, add_color=True):
        return C.color(text, C.cokgreen, add_color)

    @staticmethod
    def warning(text, add_color=True):
        return C.color(text, C.cwarning, add_color)

    # Add more color methods as needed