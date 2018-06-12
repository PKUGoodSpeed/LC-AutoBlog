#!/usr/bin/env python3
import os
import json
from web_src.utils import ColorMessage
from web_src.index import makeSearchIndex

def _setupDirs(json_file):
    C = json.load(open(json_file, 'r'))
    title_file = C['title_file']
    local_dir = C["local_dir"]
    target_dir = C["target_dir"]
    target_web = C["target_web"]
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
    makeSearchIndex(target_dir, target_web, templates + "/base.html")
    ColorMessage("Setup Index Page Finished.", "magenta")
    


if __name__ == "__main__":
    json_file = "./configs/setup.json"
    _setupDirs(json_file)