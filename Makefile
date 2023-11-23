run:
	uvicorn app.main:app --reload

build:
	pdm list --freeze >> requirements.txt
	docker build . -t fastapi-htmx
	rm requirements.txt
