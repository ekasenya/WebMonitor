#!/bin/bash

arg=$1

run_dev () {
  echo "Start running \"dev\" environment..."
  docker-compose down -v
  cp ./deploy/docker-compose.dev.yaml docker-compose.yaml
  build
  docker-compose up
}

run_prod () {
  echo "Start running \"prod\" environment..."
  docker-compose down -v
  cp ./deploy/docker-compose.prod.yaml docker-compose.yaml
  build

  docker-compose up
}

build () {
  echo "Start building services..."
  docker-compose build
  echo "Completed"
}


case "$arg" in
    prod)
		run_prod
		;;
    *)
    run_dev
		;;
esac