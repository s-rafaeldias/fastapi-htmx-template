run:
	uvicorn app.main:app --reload

run-css:
	./tailwindcss -i static/input.css -o dist/output.css --watch

build:
	pdm list --freeze >> requirements.txt
	docker build . -t fastapi-htmx
	rm requirements.txt
