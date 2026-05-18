PROJECTS := cloudbudget infraflow netguardian netaegis

.PHONY: all down test clean

all:
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
