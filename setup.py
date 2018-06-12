#!/usr/bin/env python3
import os
import json
from web_src.utils import ColorMessage

def _setupDirs(json_file):
    C = json.load(open(json_file, 'r'))
    title_file = C['title_file']
    target_dir = C["target_dir"]
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    try:
        os.chmod(target_dir, 0o777)
    except:
        msg = "Cannot change the permission level for " + target_dir
        ColorMessage(msg, "orange")
    with open(title_file, 'r') as f:
        for line in f:
            problem_dir = target_dir + "/" + line
            if not os.path.exists(problem_dir):
                os.makedirs(problem_dir)
            try:
                os.chmod(problem_dir, 0o777)
            except:
                msg = "Cannot change the permission level for " + problem_dir
                ColorMessage(msg, "orange")
        f.close()
    ColorMessage("Setup Leetcode Web Directory Finished. Please check manually as well!", "green")


if __name__ == "__main__":
    json_file = "./configs/setup.json"
    _setupDirs(json_file)