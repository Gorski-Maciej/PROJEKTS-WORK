.PHONY: all down test clean validate-env audit verify-ports check

PROJECTS = cloudbudget infraflow netguardian netaegis

all:
	@for proj in $(PROJECTS); do \
		cd $$proj && docker compose up -d && cd ..; \
	done
	@echo "All projects started"

down:
	@for proj in $(PROJECTS); do \
		cd $$proj && docker compose down && cd ..; \
	done

test:
	@echo "Tests are intentionally skipped in this workflow."

check:
	@$(MAKE) validate-env
	@$(MAKE) audit
	@$(MAKE) verify-ports

validate-env:
	@python scripts/validate_env_examples.py

audit:
	@python scripts/audit_projects.py
	@python scripts/validate_env_examples.py

verify-ports:
	@./verify_all_ports.sh

clean:
	@for proj in $(PROJECTS); do \
		cd $$proj && docker compose down -v && cd ..; \
	done
