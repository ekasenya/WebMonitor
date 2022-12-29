#!/usr/bin/env bash
python3 -m web_monitor.main \
-c "web_monitor/configs/development.yaml" \
--source_filename "web_monitor/data/url_list.json" \
--frequency 20