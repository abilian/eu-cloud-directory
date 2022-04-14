WIP website for the Euclidia Cloud Directory
============================================


## How to install / build ?


1) Checkout https://github.com/Fonds-de-Dotation-du-Libre/european-cloud-industry in the `data/` directory
(symlinks work also).

2) Create and activate a Python virtualenv. Make sure you have installed Poetry.

3) Run `poetry install`

4) Run `make build`.

5) The content of the website is in the "build" directory. 

You may run a local webserver with: `python -m http.server 8000` from this directory.

6) Point your browser to http://localhost:8000/
