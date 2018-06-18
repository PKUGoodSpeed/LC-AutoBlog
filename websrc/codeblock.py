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
pd.set_option("display.max_colwidth", -1)


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
        "runtime": [solu['runtime'] for solu in solutions],
        "percentage": [solu['percentage'] for solu in solutions],
    })
    question_addr = target_addr + "/" + title
    df = df[["nickname", "language", "complexity", "runtime", "percentage"]]
    df["nickname"] = df["nickname"].apply(
        lambda x: getHtmlElement(
            tag='a', msg=x, selfclose=False, href="\'{LINK}\'".format(LINK=question_addr + "/" + x + ".html")))
    solu_html_table = df.to_html(index=None, escape=False, classes="sortable")
    q_desc = markdown(description)
    return template.render(
        styles = getIndexStyle(font="Comic Sans MS", theme="white", boxcolor="gray", hovercolor="orange", fontweight="500"),
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
        styles = getIndexStyle(font="Comic Sans MS", theme="white", boxcolor="gray", hovercolor="orange", fontweight="500"),
        NAVS=navs, Q_title=title, S=solution, S_desc=description)
