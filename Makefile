install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	pytest -vv --cov=app --cov=utils test_*.py

format:
	black . *.py

lint:
	pylint --disable=R,C *.py utils/*.py

container-lint:
	docker run -rm -i hadolint/hadolint < Dockerfile

refactor:
	format lint

run:
	stremalit run app.py

deploy:
#echo "deploy not implemented"

all: install lint test format deploy
