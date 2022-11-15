COMPOSE_UP=docker-compose up
COMPOSE_DOWN=docker-compose down
IMAGES=lab5-nginx lab5-php lab5-uwsgi
start:
	$(COMPOSE_UP)  
stop:
	$(COMPOSE_DOWN)
clean:
	docker image rm $(IMAGES)