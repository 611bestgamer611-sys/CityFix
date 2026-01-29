.PHONY: help build up down logs clean restart

help:
	@echo "CityFix - Comandi disponibili:"
	@echo "  make build      - Build di tutti i container"
	@echo "  make up         - Avvia tutti i servizi"
	@echo "  make down       - Ferma tutti i servizi"
	@echo "  make logs       - Visualizza i logs"
	@echo "  make clean      - Rimuove container e volumi"
	@echo "  make restart    - Riavvia tutti i servizi"

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

clean:
	docker-compose down -v
	docker system prune -f

restart:
	docker-compose restart