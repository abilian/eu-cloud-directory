#!/usr/bin/env python3

import glob
import json
import os

from jinja2 import Environment, select_autoescape, FileSystemLoader
from .load import providers, solutions, read_data

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


def build():
    vite_build()
    read_data()
    generate_pages()
