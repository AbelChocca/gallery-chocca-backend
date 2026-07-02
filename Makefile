.PHONY: dev-up dev-down test test-file test-supply

dev-up:
	docker compose -f docker-compose.dev.yml up -d --build

test-down:
	docker compose -f docker-compose.dev.yml down

test-up:
	docker compose -f docker-compose.test.yml up -d --build

test-down:
	docker compose -f docker-compose.test.yml down

test:
	pytest -v

test-file:
	pytest $(FILE) -v --durations=0 -s

test-k:
	pytest -v -k "$(KEYWORD)"

test-search:
	pytest $(FILE) -v -k "$(KEYWORD)"