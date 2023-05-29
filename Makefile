DEFAULT_COMMAND=python main.py
DEFAULT_BUILD_COMMAND=$(DEFAULT_COMMAND) blog.txt blog.html

install: # Install dependencies
	pip install -r requirements.txt

build: # Single build
	$(DEFAULT_BUILD_COMMAND)

watch: # Watch for changes
	$(DEFAULT_BUILD_COMMAND) -w

help:
	$(DEFAULT_COMMAND) --help
