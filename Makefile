.PHONY: all down test clean

all:
	@for proj in cloudbudget infraflow netguardian netaegis; do \
	 cd $$proj && docker compose up -d && cd ..; \
	done
	@echo "All projects started"

down:
	@for proj in cloudbudget infraflow netguardian netaegis; do \
	 cd $$proj && docker compose down && cd ..; \
	done

test:
	@for proj in cloudbudget infraflow netguardian netaegis; do \
	 cd $$proj && python -m pytest tests/ -v || true; cd ..; \
	done

clean:
	@for proj in cloudbudget infraflow netguardian netaegis; do \
	 cd $$proj && docker compose down -v && cd ..; \
	done
