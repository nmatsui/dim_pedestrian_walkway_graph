#!/bin/bash

docker run -it -v $(pwd)/config:/opt/config -v $(pwd)/data_files:/opt/data_files data_importer:0.1.0 -c /opt/config/fiware_config.json -t node $1
