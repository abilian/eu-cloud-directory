#!/usr/bin/env python3

import glob
import json

providers = {}
solutions = {}


def read_data():
    files = glob.glob("data/*.json")

    for file in sorted(files):
        try:
            provider = json.load(open(file))
        except:
            print(f"failed to read {file}")
            continue

        provider_name = provider["title"]
        provider["id"] = file.split("/")[1][0:-len(".json")]
        providers[provider_name] = provider

        for solution in provider["solution_list"]:
            if not isinstance(solution, dict):
                continue
            if not "title" in solution:
                continue
            solution_name = solution["title"]
            solutions[solution_name] = solution

        try:
            provider["solution_list"] = sorted(provider["solution_list"], key=lambda x: x['title'])
        except:
            pass
