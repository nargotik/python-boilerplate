# Identify Docker
BIN_DOCKER_COMPOSE:=$(shell which docker-compose)
ifeq ($(strip $(BIN_DOCKER_COMPOSE)),)
BIN_DOCKER_COMPOSE=$(BIN_DOCKER) compose
endif
BIN_DOCKER:=$(shell which docker)


# HELP
# This will output the help for each task
# thanks to https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.PHONY: help

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

stop: ## Stop and remove the container and network.
	$(BIN_DOCKER_COMPOSE) down

start: ## Run the container.
	$(BIN_DOCKER_COMPOSE) up -d --remove-orphans

bash: ## Interactive container bash.
	$(BIN_DOCKER) exec -ti $(PROJECT_NAME) bash
