start:
	docker compose up --build

stop:
	docker compose down -v

server-it:
	docker compose exec -it server sh

client_it:
	docker compose exec -it client sh