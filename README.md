[![Github Actions Workflow](https://github.com/DiogoCarapito/mgfhub2/actions/workflows/main.yaml/badge.svg)](https://github.com/DiogoCarapito/mgfhub2/actions/workflows/main.yaml)

# mgfhub2
mgfhub 2.0 with streamlit


## cheat sheet
###  venv
create venv
```bash
python3 -m venv .venv
```
activate venv
```bash
source .venv/bin/activate
```

### Dockerfile
build
```bash
docker build -t app:latest .
````
check image id
```bash
docker images
````
run with image id
```bash
docker run -p 8501:8501 app:latest
````