rev:
ifndef m
	$(error m is requied)
endif
	alembic revision --autogenerate -m "$(m)"

up:
	alembic upgrade head

down:
	alembic downgrade base
