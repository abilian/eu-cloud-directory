.PHONY: build
build:
	poetry run build


clean:
	rm -rf vite/dist


deploy: build
	rsync -e ssh -avz build/ web@bulma:/srv/web/eu-cloud-directory.lab.abilian.com/


update:
	cd data && git pull


install:
	poetry install
	yarn --cwd vite install

