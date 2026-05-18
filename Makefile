PROJECTS := cloudbudget infraflow netguardian netaegis

.PHONY: all up down test clean

all: up

up:
	@for p in $(PROJECTS); do \
		echo "[up] $$p"; \
		cd $$p && bash scripts/setup.sh && docker compose up -d || exit 1; \
		cd - >/dev/null; \
	done

down:
	@for p in $(PROJECTS); do \
		echo "[down] $$p"; \
		cd $$p && docker compose down || exit 1; \
		cd - >/dev/null; \
	done

test:
	@for p in $(PROJECTS); do \
		echo "[test] $$p"; \
		if [ -d $$p/tests ]; then cd $$p && pytest -q || exit 1; cd - >/dev/null; else echo "no tests dir"; fi; \
	done

clean:
	@for p in $(PROJECTS); do \
		echo "[clean] $$p"; \
		cd $$p && docker compose down -v --remove-orphans || true; \
		cd - >/dev/null; \
	done
