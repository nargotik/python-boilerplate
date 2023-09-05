TAG_COMMIT := $(shell git rev-list --abbrev-commit --tags --max-count=1)
# `2>/dev/null` suppress errors and `|| true` suppress the error codes.
TAG := $(shell git describe --abbrev=0 --tags ${TAG_COMMIT} 2>/dev/null || true)
COMMIT := $(shell git rev-parse --short HEAD 2>/dev/null || true)
# here we strip the version prefix
VERSION := $(TAG:v%=%)
COMMIT := $(COMMIT:v%=%)


# HELP
# This will output the help for each task
# thanks to https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.PHONY: help

-include $(PWD)/.env

BRANCH := $(CI_COMMIT_BRANCH)
HASH := $(CI_COMMIT_SHORT_SHA)
REGISTRY = $(DOCKER_REGISTRY)

ifeq ($(BRANCH),main)
   TAG = latest
else
   TAG = debug
endif
TAG2 = $(HASH)


SNAME ?= $(CI_PROJECT_PATH)
VER ?= `cat VERSION`
BASENAME ?= python:3.11
TARGET_PLATFORM ?= linux/amd64,linux/arm64
# linux/amd64,linux/arm64,linux/ppc64le,linux/s390x,linux/386,linux/arm/v7,linux/arm/v6
NO_CACHE ?=
# NO_CACHE ?= --no-cache
#MODE ?= debug
MODE ?= $(VER)


# Identify Docker
BIN_DOCKER_COMPOSE:=$(shell which docker-compose)
ifeq ($(strip $(BIN_DOCKER_COMPOSE)),)
BIN_DOCKER_COMPOSE=$(BIN_DOCKER) compose
endif
BIN_DOCKER:=$(shell which docker)

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

build: ## Build the container
	mkdir -p builds
	DOCKER_BUILDKIT=1 $(BIN_DOCKER) build $(NO_CACHE) \
	-t $(REGISTRY)$(SNAME):$(VER) -t $(REGISTRY)$(SNAME):$(TAG) \
	--build-arg BUILD_DATE=`date -u +"%Y-%m-%dT%H:%M:%SZ"` \
	--build-arg VCS_REF=`git rev-parse --short HEAD` \
	--build-arg BASEIMAGE=$(BASENAME) \
	.

buildx: ## Buildx the container
	$(BIN_DOCKER) buildx build $(NO_CACHE) \
	--platform ${TARGET_PLATFORM} \
	-t $(REGISTRY)$(SNAME):$(VER) -t $(REGISTRY)$(SNAME):$(TAG) \
	--pull --push \
	--build-arg BUILD_DATE=`date -u +"%Y-%m-%dT%H:%M:%SZ"` \
	--build-arg VCS_REF=`git rev-parse --short HEAD` \
	--build-arg BASEIMAGE=$(BASENAME) \
	--build-arg VERSION=$(VER) \
	.


stop: ## Stop and remove the container and network.
	make -C deploy stop

start: ## Build and run the container.
	make -C deploy start
