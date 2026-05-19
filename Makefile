PROJECTS := cloudbudget infraflow netguardian netaegis

.PHONY: validate-env check-docker all down test clean

validate-env:
	@for proj in cloudbudget infraflow netguardian netaegis; do \
	 if [ -f $$proj/.env ]; then \
	  SECRET=$$(grep JWT_SECRET $$proj/.env | cut -d '=' -f2); \
	  if [ $${#SECRET} -lt 32 ] || [ "$$SECRET" = "change_me_32_chars_min" ]; then \
	   echo "ERROR: $$proj JWT_SECRET is too short or default"; \
	   exit 1; \
	  fi; \
	 fi; \
	done
	@echo "All JWT_SECRETS valid"

check-docker:
	@which docker > /dev/null || (echo "Docker not found"; exit 1)
	@docker info > /dev/null 2>&1 || (echo "Docker daemon not running"; exit 1)
	@echo "Docker OK"

all: validate-env check-docker
	@for project in $(PROJECTS); do (cd $$project && docker compose up -d); done

down:
	@for project in $(PROJECTS); do (cd $$project && docker compose down); done

test:
	@for project in $(PROJECTS); do (cd $$project && pytest); done

clean:
	@for project in $(PROJECTS); do (cd $$project && docker compose down -v --rmi all); done
