start:
	docker compose up --build

stop:
	docker compose down -v

.PHONY: server
server:
	docker compose exec -it server sh

.PHONY: client
client:
	docker compose exec -it client sh
