#!/bin/bash

docker run -it -v $(pwd)/config:/opt/config -v $(pwd)/data_files:/opt/data_files test:0.0.1 -c /opt/config/fiware_config.json -t link $1
