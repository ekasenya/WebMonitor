#!/bin/bash

pytest data_handler/tests
if [[ $? -eq 0 ]]
then
  python3 -m web_monitor.main \
-c "web_monitor/configs/development.yaml" \
fi;

