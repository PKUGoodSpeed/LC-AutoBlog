#!/usr/bin/env python3
import os
import json
from websrc.utils import ColorMessage, ProgressBar
from websrc.index import makeSearchIndex
from autoblog.database import getDataBase, initDataBase

progressbar = ProgressBar()

def _setupDirs(C):
    title_file = C['title_file']
    local_dir = C["local_dir"]
    target_dir = C["target_dir"]
    target_web = C["target_web"]
    if target_web[-1] != "/":
        target_web += "/"
    templates = C["templates"]
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    try:
        os.chmod(target_dir, 0o777)
    except:
        msg = "Cannot change the permission level for " + target_dir
        ColorMessage(msg, "red")
    with open(title_file, 'r') as f:
        for line in f:
            line = line.replace("\n", "")
            problem_dir = target_dir + "/" + line
            if not os.path.exists(problem_dir):
                os.makedirs(problem_dir)
            local_problem_dir = local_dir + "/" + line
            if not os.path.exists(local_problem_dir):
                os.makedirs(local_problem_dir)
            try:
                os.chmod(problem_dir, 0o777)
            except:
                msg = "Cannot change the permission level for " + problem_dir
                ColorMessage(msg, "red")
    ColorMessage("Setup Leetcode Web Directory Finished. Please check manually as well!", "magenta")
    makeSearchIndex(target_dir, target_web, templates + "/index.html")


def _setupDesc(C):
    local_dir = C["local_dir"]
    if not os.path.exists(local_dir):
        ColorMessage("Local workspace should be setup first!", "red")
    else:
        ColorMessage("Creating question descriptions using leetcode-cli ... (leetcode-cli version > 2 is needed)", "cyan")
        folders = [f for f in os.listdir(local_dir) if f[0] == "["]
        success_cnt = 0
        for f in folders:
            if f[0] != '[':
                continue
            pdir = local_dir + "/" + f
            qstn = f[1:].split("]")[0]
            stat = os.system("leetcode show {N} > {F}".format(
                N=qstn, F=pdir + "/README.md"))
            if not stat:
                success_cnt += 1
                ColorMessage("Generating description for " + f + " succeed!", "green")
            else:
                ColorMessage("Warning: Generating description for " + f + " failed!", "red")
        msg = "\n\n" + "="*20
        ColorMessage(msg, "cyan")
        msg = "Success: {D}/{N}".format(D=str(int(success_cnt)), N=str(int(len(folders))))
        ColorMessage(msg, "cyan")
        ColorMessage("Description setup finished!", "cyan")


if __name__ == "__main__":
    json_file = "./configs/setup.json"
    C = json.load(open(json_file, 'r'))
    _setupDirs(C)
    # _setupDesc(C)
