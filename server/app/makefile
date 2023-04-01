alembic:
ifndef m
	$(error m is requied)
endif
	alembic revision --autogenerate -m "$(m)"

alembic_up:
	alembic upgrade head

alembic_down:
	alembic downgrade base
