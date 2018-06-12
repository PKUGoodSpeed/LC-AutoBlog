"""
Making an index page with search Engine for the Leetcode root folder
@author: pkugoodspeed
@date: 06/12/2018
@copyright: jogchat.com
"""
import os
from jinja2 import Template
from .utils import ColorMessage, getHtmlElement


def _getIndexStyle():
    return """* {
              box-sizing: border-box;
            }
            
            #Input {
              background-position: 10px 12px;
              background-repeat: no-repeat;
              width: 100%;
              font-size: 16px;
              padding: 12px 20px 12px 40px;
              border: 1px solid #ddd;
              margin-bottom: 12px;
            }

            #navi {
                list-style-type: none;
                margin: 0;
                padding: 0;
                overflow: hidden;
                background-color: #334;
            }
            
            #navi li {
                float: left;
            }
            
            #navi li a {
                display: block;
                color: white;
                text-align: center;
                padding: 14px 16px;
                text-decoration: none;
            }
            
            #navi li div {
                display: block;
                color: white;
                text-align: center;
                padding: 14px 16px;
                text-decoration: none;
            }
            
            #navi li a:hover {
                background-color: #111;
            }

            #folders {
              list-style-type: none;
              padding: 0;
              margin: 0;
            }
            
            #folders li a {
              border: 1px solid #ddd;
              margin-top: -1px; /* Prevent double borders */
              background-color: #b6b6b6;
              padding: 8px;
              text-decoration: none;
              font-size: 17px;
              color: black;
              display: block
            }
            
            #folders li a:hover:not(.header) {
              background-color: #fff;
            }
    """


def _getSearchScripts():
    """
    Here we only consider folders
    """
    return """
        function _check(filename, keywords) {
                var i;
                var l = keywords.length;
                for(i = 0; i < l; i++){
                    if(filename.indexOf(keywords[i]) == -1){
                        return false;
                    }
                }
                return true;
            }
            function _filter() {
                var input, keywords, ul, li, len_li, filename, i;
                input = document.getElementById("Input");
                keywords = input.value.toUpperCase().split(" ");
                ul = document.getElementById("folders");
                li = ul.getElementsByTagName("li");
                len_li = li.length;
                for (i = 0; i < len_li; i++) {
                    filename = li[i].getElementsByTagName("a")[0].innerHTML.toUpperCase();
                    if (_check(filename, keywords)) {
                        li[i].style.display = "";
                    } else {
                        li[i].style.display = "none";
                    }
                }
            }
    """

def _getIndexBody(path, addr):
    if not os.path.exists(path):
        ColorMessage(path + " does not exist!", "red")
    folders = [f for f in os.listdir(path) if os.path.isdir(path + "/" + f) and f[0] == "["]
    folders.sort(key=lambda x: int(x[1:].split("]")[0]))
    hl_folders = [getHtmlElement(
        tag='a', selfclose=False, msg=f, href="\"{ADDR}/{F}\"".format(ADDR=addr, F=f), target="\"_self\"") for f in folders]
    li_folders = [getHtmlElement(tag='li', msg=f) for f in hl_folders]

    body = getHtmlElement(tag="h1", msg="Problems") + "\n"
    body += getHtmlElement(
        tag="input", msg="", selfclose=True, type="\"text\"", id="\"Input\"",
        onkeyup="\"_filter()\"", placeholder="\"Search for keywords...\"", title="\"SE\"") + "\n"
    body += getHtmlElement(tag='ul', msg="\n".join(li_folders), selfclose=False, id="\"folders\"")
    return body


def makeSearchIndex(path, addr, template_file="./templates/base.html"):
    """ Creating a index.html page for problem directory """
    ColorMessage("Generating Index Page for " + addr + "...", "cyan")
    f = open(template_file, 'r')
    template = Template(f.read())
    f.close()
    index_file = path + "/index.html"
    if os.path.exists(index_file):
        os.remove(index_file)
    ColorMessage("\tGetting styles...", "cyan")
    styles=_getIndexStyle()
    ColorMessage("\tGetting page contents...", "cyan")
    page_body=_getIndexBody(path, addr)
    ColorMessage("\tGetting search scripts...", "cyan")
    page_scripts = _getSearchScripts()
    try:
        with open(path + "/index.html", "w") as idx:
            idx.write(template.render(
                styles=styles,
                page_body=page_body,
                page_scripts=page_scripts))
        ColorMessage("Creating index page succeed!", "cyan")
    except:
        ColorMessage("Creating index page failed!", "red")
    try:
        os.chmod(path + "/index.html", 0o777)
        ColorMessage("Changing permission level succeed!", "cyan")
    except:
        ColorMessage("Changing permission level failed!", "red")
