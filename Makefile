SHELL := /usr/bin/env bash

.PHONY: help generate-from-nn nn-build demo-check setup demo-start demo-stop

help:
	@echo "Targets:"
	@echo "  make generate-from-nn  - generate missing bootstrap/demo files from _nn.txt guidance"
	@echo "  make demo-check        - validate demo prerequisites and compose configs"
	@echo "  make setup             - run per-project setup scripts"
	@echo "  make demo-start        - setup + start all demo stacks"
	@echo "  make demo-stop         - stop all demo stacks"

generate-from-nn:
	python tools/generate_from_nn.py --sync --source _nn.txt

demo-check:
	./scripts/demo_doctor.sh

setup:
	./setup.sh

demo-start:
	./run_all_demos.sh --with-setup

demo-stop:
	./stop_all_demos.sh


nn-build:
	python tools/nn_build_project.py --source _nn.txt
