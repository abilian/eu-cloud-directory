.PHONY: build
build:
	./build.py


clean:
	rm -rf vite/dist


push: build
	rsync -e ssh -avz build/ web@bulma:/srv/web/eu-cloud-directory.lab.abilian.com/
