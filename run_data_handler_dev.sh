#!/bin/bash

pytest data_handler/tests
if [[ $? -eq 0 ]]
then
  python3 -m data_handler.main \
-c "./data_handler/configs/development.yaml" \
fi;
