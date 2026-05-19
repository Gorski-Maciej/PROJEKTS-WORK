PROJECTS := cloudbudget infraflow netguardian netaegis

.PHONY: validate-env all down test clean

validate-env:
	@set -e; \
	for project in $(PROJECTS); do \
		if [ ! -f $$project/.env ]; then echo "Missing $$project/.env"; exit 1; fi; \
		if [ ! -f $$project/.env.example ]; then echo "Missing $$project/.env.example"; exit 1; fi; \
	done; \
	for project in cloudbudget infraflow netguardian; do \
		jwt=$$(grep -E "^JWT_SECRET=" $$project/.env | cut -d= -f2- || true); \
		if [ -z "$$jwt" ] || [ "$$jwt" = "change_me_32_chars_min" ] || [ "$$jwt" = "local_dev_jwt_secret_replace_me_32chars_min" ] || [ "$$jwt" = "cloudbudget_local_jwt_secret_please_change" ] || [ "$$jwt" = "infraflow_local_jwt_secret_please_change" ] || [ "$$jwt" = "netguardian_local_jwt_secret_please_change" ]; then echo "Invalid JWT_SECRET in $$project/.env"; exit 1; fi; \
	done

all: validate-env
	@for project in $(PROJECTS); do \
		(cd $$project && docker compose up -d); \
	done

down:
	@for project in $(PROJECTS); do \
		(cd $$project && docker compose down); \
	done

test:
	@for project in $(PROJECTS); do \
		(cd $$project && pytest); \
	done

clean:
	@for project in $(PROJECTS); do \
		(cd $$project && docker compose down -v --rmi all); \
	done
