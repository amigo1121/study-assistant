rev:
ifndef m
	$(error m is requied)
endif
	alembic revision -m "$(m)"

up:
	alembic upgrade head

down:
	alembic downgrade base
