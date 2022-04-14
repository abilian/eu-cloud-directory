#!/usr/bin/env python3

import glob
import json
import os

from devtools import debug
from jinja2 import Environment, select_autoescape, FileSystemLoader

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


def generate_page(template, name, ctx):
    env = Environment(
        loader=FileSystemLoader("templates"),
        autoescape=select_autoescape()
    )
    template = env.get_template(template)

    js_file = glob.glob("vite/dist/assets/*.js")[0].split("/")[-1]
    css_file = glob.glob("vite/dist/assets/*.css")[0].split("/")[-1]
    vite_assets = f"""
        <script type="module" crossorigin src="/assets/{js_file}"></script>
        <link rel="stylesheet" href="/assets/{css_file}">
    """
    ctx["vite_assets"] = vite_assets
    result = template.render(**ctx)
    with open(f"build/{name}", "w") as output:
        output.write(result)


def generate_pages():
    ctx = {'providers': providers.values(), 'solutions': solutions.values()}
    ctx["title"] = "European Cloud Technologies Directory"
    generate_page("index.j2", "index.html", ctx)

    for provider in providers.values():
        id = provider["id"]
        ctx = {"provider": provider, "title": f"Company: {provider['title']}"}
        generate_page("provider.j2", f"providers/{id}.html", ctx)

    # for name, solution in solutions.items():
    #     generate_page("solution.tpl", f"solutions/{name}.html")


def vite_build():
    os.system("yarn --cwd vite build")
    os.system("cp -r vite/dist/assets build/")


def main():
    vite_build()
    read_data()
    generate_pages()


main()
