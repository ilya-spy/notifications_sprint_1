ifndef VERBOSE
.SILENT:
endif
.DEFAULT_GOAL := help

ifeq ($(OS),)
OS := $(shell uname)
endif


#
# Cписок доступных команд
#
help:
	@grep -E '^[a-zA-Z0-9_\-\/]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'
	@echo "(Other less used targets are available, open Makefile for details)"
.PHONY: help


#
# Команды развёртывания полного Notifications стенда
# (все сервисы вместе, ниже есть команды для запуска отдыльных сервисов)
#
notifications/dev/setup:
	make admin/dev/setup
	make worker/dev/setup
	make frontend/dev/setup
.PHONY: notifications/dev/setup

notifications/prod/teardown:
	make worker/dev/teardown
	make admin/dev/teardown
	make frontend/dev/teardow
.PHONY: notifications/dev/teardown


#
# Команды развертывания и доступа в службы внешнего api notifications
#
admin/%: export DOCKER_DIR := devops/frontend

admin/dev/%: export DOCKER_TARGET := dev
admin/prod/%: export DOCKER_TARGET := prod


#
# Команды развертывания и доступа в службы worker
#
worker/%: export DOCKER_DIR := devops/worker

worker/dev/%: export DOCKER_TARGET := dev
worker/prod/%: export DOCKER_TARGET := prod

worker/mailer:
	@docker exec -it worker-mailer bash

#
# Команды развертывания и доступа в службы admin
#
admin/%: export DOCKER_DIR := devops/admin

admin/dev/%: export DOCKER_TARGET := dev
admin/prod/%: export DOCKER_TARGET := prod


#
# Шаблоны-команды для запуска и остановки сервисов через docker-composer
#
%/dev/setup:
	@make docker/prepare
	@make docker/setup
.PHONY: %/dev/setup

%/prod/setup:
	@make docker/prepare
	@make docker/setup
.PHONY: %/prod/setup

%/dev/teardown:
	@make docker/prepare
	@make docker/destroy
.PHONY: %/teardown/dev

%/prod/teardown:
	@make docker/prepare
	@make docker/destroy
.PHONY: %/prod/teardown



#
#  Базовые команды для сборки и запуска заданных Докер-контейнеров (разные цели сборки выше задают $DOCKER_DIR / $DOCKER_TARGET / $DEVOPS_DIR)
#
docker/%: export DOCKER_COMPOSE := docker-compose -f $(DOCKER_DIR)/docker-compose.yml -f $(DOCKER_DIR)/docker-compose.$(DOCKER_TARGET).yml --env-file devops/docker/.env

docker/prepare:
	printf "Setting up local environment: $(OS)\n"
	find devops -name '.env.example' | xargs -I {} sh -c 'cp $${1} $${1/.env.example/.env}' -- {}
	
	printf "Create common network environment: yp_network\n"
	docker network create --driver bridge yp_network || true

	# установить HOST_UID = UID текущего пользователя. Это влияет на UID пользователя внутри контейнера.
	# Нужно для совместимости прав доступа к сгенерированным файлам у хостового пользователя
	# На Windows host также необходимо переформатирование команд (кавычки и т.д.)
	if [[ $(OS) = 'Darwin' ]]; then \
		`id -u | xargs -I '{}' sed -i '' 's/HOST_UID=.*/HOST_UID={}/' devops/docker/.env`; \
		`sed -i '' 's/HOST_GID=.*/HOST_GID=61/' devops/docker/.env`; \
	elif [[ $(OS) = 'Windows_NT' ]]; then \
		`id -u | xargs -I '{}' sed -i "s/HOST_UID=.*/HOST_UID={}/" devops/docker/.env`; \
		`id -g | xargs -I '{}' sed -i "s/HOST_GID=.*/HOST_GID={}/" devops/docker/.env`; \
	else \
		`id -u | xargs -I '{}' sed -i '' 's/HOST_UID=.*/HOST_UID={}/' devops/docker/.env`; \
		`id -g | xargs -I '{}' sed -i '' 's/HOST_GID=.*/HOST_GID={}/' devops/docker/.env`; \
	fi
	printf "Set up environment for: $(DOCKER_TARGET)\n"
	printf "Invoke composer command: $(DOCKER_COMPOSE)\n"
docker/prepare:
.PHONY: docker/prepare

## перестроить и перезапустить контейнеры
docker/setup:
	make docker/destroy
	make docker/build
	make docker/start
docker/setup:
.PHONY: docker/setup

## построить контейнеры
docker/build:
	$(DOCKER_COMPOSE) build
.PHONY: docker/build

## поднять Докер
docker/start:
	$(DOCKER_COMPOSE) up -d
.PHONY: docker/start

# алиас для docker/start
docker/up: docker/start
.PHONY: docker/up

## остановить все контейнеры
docker/stop:
	$(DOCKER_COMPOSE) down
.PHONY: docker/stop

## остановить и удалить все контейнеры
docker/down:
	$(DOCKER_COMPOSE) down --remove-orphans
.PHONY: docker/down

## остановить/удалить контейнеры и очистить данные томов
docker/destroy:
	$(DOCKER_COMPOSE) down --volumes --remove-orphans
.PHONY: docker/destroy

#
#  Команды настройки локального девелопмент окружения
#
pipenv/%:
	find devops -name 'base.txt' | xargs -I {} sh -c 'pipenv install -r $${1}' -- {}
pipenv/dev/setup:
	find devops -name 'dev.txt' | xargs -I {} sh -c 'pipenv install -r $${1}' -- {}
pipenv/prod/setup:
	find devops -name 'prod.txt' | xargs -I {} sh -c 'pipenv install -r $${1}' -- {}

