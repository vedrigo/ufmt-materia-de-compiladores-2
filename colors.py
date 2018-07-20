import platform


class Colors:
    if (platform.system() == 'Windows'):
        pink = ''
        blue = ''
        sucess = ''
        warning = ''
        danger = ''
        reset = ''
    else:
        pink = '\033[95m'
        blue = '\033[94m'
        sucess = '\033[92m'
        warning = '\033[93m'
        danger = '\033[91m'
        reset = '\033[0m'
