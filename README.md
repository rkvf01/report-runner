
Report Runner is a small Python CLI tool for generating recurring internal reports from YAML-defined data sources.

- cli.py 
 - runner/config.py:loadconfig loads YAML file and returns dict
 - calls loadconfig and gets the dictionary from the yaml file which is the path input.
 - parses the sources -> which has summary(also a dict with type and path)ie yaml.sources.summary.path and yaml.sources.summary.type
 - check if type is a file
	- call the source/file.py: fetch_file_source(dict: sources.summary)
 - fetch_file_source :  gets the path from input, validates filefound and loads as json and returns it.
 - call the template render function with yaml_config['template'] , and json returned from the fetch_file_source .ie the json file in yaml.sources.summary.path

## Current Status

This project is in early MVP development.

Currently supported:

- YAML-based report configuration
- File-based JSON source
- Jinja2 HTML template rendering
- Dry-run mode
- CLI using Typer

## Install Locally

```bash
pip3 install -e .

example run:
report-runner run reports/examples/monthly-security-posture.yaml --dry-run

Why This Exists

Many teams still create recurring reports manually by querying systems, copying results, formatting emails, and sending updates. Report Runner aims to make that process repeatable and automated.

The long-term goal is:

YAML report config
        ↓
Athena / REST API / file sources
        ↓
Jinja2 HTML template
        ↓
Email delivery
        ↓
Failure alerts and run history


