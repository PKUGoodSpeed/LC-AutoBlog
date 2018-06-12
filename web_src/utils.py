from termcolor import colored

def ColorMessage(msg, color):
    print(colored(msg, color))
    return None

def getHtmlElement(tag='p', msg="undefined", selfclose=False, **kwargs):
    """
    Creating an HTML element
    return <tag args>msg</tag>
    """
    element = "<" + tag
    for key, val in kwargs.items():
        element += " " + key + "=" + val
    element += ">"
    if selfclose:
        return element
    element += "{M}</{T}>".format(M=msg, T=tag)
    return element
