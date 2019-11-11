OSFLAG :=
ifeq ($(OS), Windows_NT)
	python = python
else
	python = python3
endif

clean:
	rm -rf ./src/__pycache__ ./cogs/__pycache__
install:
	$(python) -m pip install -r requirements.txt
lint:
	flake8
run:
	$(python) main.py