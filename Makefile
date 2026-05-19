PROJECTS := cloudbudget infraflow netguardian netaegis
JWT_PROJECTS := cloudbudget infraflow netguardian

.PHONY: validate-env check-docker all down test clean

validate-env:
	@set -e; \
	for project in $(PROJECTS); do \
		if [ ! -f $$project/.env ]; then echo "Missing $$project/.env"; exit 1; fi; \
		if [ ! -f $$project/.env.example ]; then echo "Missing $$project/.env.example"; exit 1; fi; \
	done; \
	for project in $(JWT_PROJECTS); do \
		jwt=$$(grep -E "^JWT_SECRET=" $$project/.env | cut -d= -f2- || true); \
		if [ -z "$$jwt" ]; then echo "Missing JWT_SECRET in $$project/.env"; exit 1; fi; \
		if [ $${#jwt} -lt 32 ]; then echo "JWT_SECRET too short in $$project/.env"; exit 1; fi; \
		case "$$jwt" in \
			change_me_32_chars_min|local_dev_jwt_secret_replace_me_32chars_min|cloudbudget_local_jwt_secret_please_change|infraflow_local_jwt_secret_please_change|netguardian_local_jwt_secret_please_change|CHANGE_ME_IN_PRODUCTION*) \
				echo "JWT_SECRET is placeholder in $$project/.env"; exit 1;; \
		esac; \
	done; \
	./scripts/verify-no-env-in-git.sh

check-docker:
	@docker --version >/dev/null
	@docker compose version >/dev/null

all: validate-env check-docker
	@for project in $(PROJECTS); do (cd $$project && docker compose up -d); done

down:
	@for project in $(PROJECTS); do (cd $$project && docker compose down); done

test:
	@for project in $(PROJECTS); do (cd $$project && pytest); done

clean:
	@for project in $(PROJECTS); do (cd $$project && docker compose down -v --rmi all); done
