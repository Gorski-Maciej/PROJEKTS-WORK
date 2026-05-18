PROJECTS=cloudbudget infraflow netguardian netaegis

all:
	@for p in $(PROJECTS); do docker compose -f $$p/docker-compose.yml up -d --build; done

down:
	@for p in $(PROJECTS); do docker compose -f $$p/docker-compose.yml down; done

test:
	@for p in $(PROJECTS); do (cd $$p && pytest -q tests/test_health.py --import-mode=importlib || exit 1); done
