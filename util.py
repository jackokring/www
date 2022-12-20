# utilities and classes for factoring processing to make app read ok
from markdown import markdown

def markHtml(input):
    """transform to html from markdown"""
    return markdown(input)

def ANSIColor(name):
    """ANSI terminal colour sequences"""
    dict = {
        'blue': '34m',
        'red': '31m',
        'magenta': '35m',
        'green': '32m',
        'cyan': '36m',
        'yellow': '33m',
        'white': '37m',
        'none': '0m'
    }
    return '\e[' + dict.get(name)

