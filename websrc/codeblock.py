"""
Making an webpages for questions and solutions
@author: pkugoodspeed
@date: 06/12/2018
@copyright: jogchat.com
"""
import os
import pandas as pd
from jinja2 import Template
from markdown2 import markdown
from .utils import ColorMessage, getHtmlElement
from .index import getIndexStyle


def getQuestionPage(title, description, solutions, template_file, target_addr):
    """ getting Question Page """
    f = open(template_file, 'r')
    template = Template(f.read())
    f.close()
    navs = []
    navs.append({'link': target_addr, "msg": "Index"})
    df = pd.DataFrame({
        "nickname": [solu['nickname'] for solu in solutions],
        "language": [solu['language'] for solu in solutions],
        "complexity": [solu['complexity'] for solu in solutions],
        "runtime: [solu['runtime'] for solu in solutions],
        "percentage": [solu['percentage'] for solu in solutions],
    })
    question_addr = target_addr + "/" + title
    df["nickname"] = df["nickname"].apply(
        lambda x: getHtmlElement(
            tag='a', msg=x, selfclose=False, href="\'{LINK}\'".format(LINK=question_addr + "/" + x + ".html")))
    solu_html_table = df.to_html(index=None, escape=False, classes="sortable")
    q_desc = markdown(description)
    return template.render(
        NAVS=navs, Q_title=title, Q_desc=q_desc, Solu_table=solu_html_table)


def getSolutionPage(title, solution, template_file, target_addr):
    """ getting Solution Page """
    f = open(template_file, 'r')
    template = Template(f.read())
    f.close()
    navs = []
    navs.append({'link': target_addr, "msg": "Index"})
    question_addr = target_addr + "/" + title
    navs.append({'link': question_addr, "msg": "Question"})
    description = markdown(solution['interpretation'])
    return template.render(
        NAVS=navs, Q_title=title, S=solution, S_desc=description)


def getIndexStyle(font="Chalkduster", theme="silver", boxcolor="gray", hovercolor="orange"):
    return """
body {{background-color: {BODY};font-family: {FONT};}}
#Input {{background-position: 10px 12px;background-repeat: no-repeat;width: 100%;font-size: 16px;padding: 12px 20px 12px 40px;border: 1px solid #ddd;margin-bottom: 12px;}}
#folders {{list-style-type: none;padding: 0;margin: 0;}}
#folders li a {{border: 1px solid #ddd;margin-top: -1px; background-color: {BOX};padding: 8px;text-decoration: none;font-size: 17px;color: black;display: block}}
#folders li a:hover:not(.header) {{background-color: {HOVER};}}
#navi {{list-style-type: none; margin: 0; padding: 0; overflow: hidden; background-color: #334;}}
#navi li {{float: left;}}
#navi li a {{display: block; color: white; text-align: center; padding: 14px 16px; text-decoration: none;}}
#navi li div {{display: block; color: white; text-align: center; padding: 14px 16px; text-decoration: none;}}
#navi li a:hover {{background-color: #111;}}
    """.format(FONT=font, BODY=theme, BOX=boxcolor, HOVER=hovercolor)

