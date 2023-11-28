run:
	uvicorn app.main:app --reload

run-docker: build
	docker run -p 8000:80 --rm fastapi-htmx:latest


run-css:
	./tailwindcss -i static/input.css -o dist/output.css --watch

build:
	pdm export -f requirements >> requirements.txt
	docker build . -t fastapi-htmx:latest
	rm requirements.txt

build-css:
	./tailwindcss -i static/input.css -o dist/output.css --minify
