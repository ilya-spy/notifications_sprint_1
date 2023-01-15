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
notifications/prod/setup:
	make admin/prod/setup
	make sender/prod/setup
	make worker/prod/setup
.PHONY: notifications/prod/setup

notifications/prod/teardown:
	make worker/prod/teardown
	make sender/prod/teardown
	make admin/prod/teardown
.PHONY: notifications/prod/teardown


#
# Команды развертывания и доступа в службы worker
#
worker/%: export DOCKER_DIR := devops/worker

worker/dev/%: export DOCKER_TARGET := dev
worker/prod/%: export DOCKER_TARGET := prod

worker/mailer:
	@docker exec -it worker-mailer bash


#
# Шаблоны-команды для запуска и остановки сервисов через docker-composer
#
%/dev/setup:
	@make docker/prepare
	@make docker/setup
.PHONY: worker/dev/setup

%/prod/setup:
	@make docker/prepare
	@make docker/setup
.PHONY: worker/prod/setup

%/dev/teardown:
	@make docker/prepare
	@make docker/destroy
.PHONY: worker/teardown/dev

%/prod/teardown:
	@make docker/prepare
	@make docker/destroy
.PHONY: worker/prod/teardown




#
# Команды развертывания и доступа в Kafka
#
kafka/%: export DOCKER_DIR := devops/docker/etl

kafka/dev/%: export DOCKER_TARGET := dev
kafka/prod/%: export DOCKER_TARGET := prod

kafka/dev/setup:
	@make docker/prepare
	@make docker/setup
.PHONY: kafka/dev/setup

kafka/dev/teardown:
	@make docker/prepare
	@make docker/destroy
.PHONY: kafka/dev/teardown

#
# Команды развертывания и доступа в MongoDB
#
mongo/%: export DOCKER_DIR := devops/docker/mongo

mongo/dev/%: export DOCKER_TARGET := dev
mongo/prod/%: export DOCKER_TARGET := prod

mongo/dev/setup:
	@make docker/prepare
	@make docker/setup
.PHONY: mongo/dev/setup

mongo/dev/teardown:
	@make docker/prepare
	@make docker/destroy
.PHONY: mongo/dev/teardown

#
# Команды развёртывания API шлюза для отправки событий с отметками о просмотрах в Кафку
#
gate/%: export DOCKER_DIR := devops/docker/gate

gate/dev/%: export DOCKER_TARGET := dev
gate/prod/%: export DOCKER_TARGET := prod

gate/dev/setup:
	@make docker/prepare
	@make docker/setup
.PHONY: gate/dev/setup

gate/dev/teardown:
	@make docker/prepare
	@make docker/destroy
.PHONY: gate/dev/teardown


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

