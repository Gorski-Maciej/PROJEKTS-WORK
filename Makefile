PROJECTS=cloudbudget infraflow netguardian netaegis

.PHONY: all down test check-docker

check-docker:
	@command -v docker >/dev/null || (echo "Docker is required but not installed/in PATH" && exit 127)

all: check-docker
	@for p in $(PROJECTS); do docker compose -f $$p/docker-compose.yml up -d --build; done

down: check-docker
	@for p in $(PROJECTS); do docker compose -f $$p/docker-compose.yml down; done

test:
	@for p in $(PROJECTS); do (cd $$p && pytest -q tests/test_health.py --import-mode=importlib || exit 1); done
