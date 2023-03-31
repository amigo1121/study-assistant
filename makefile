start:
	docker compose up --build

stop:
	docker compose down -v

server:
	docker compose exec -it server sh

client:
	docker compose exec -it client sh