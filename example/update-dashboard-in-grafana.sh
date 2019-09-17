#!/bin/sh
echo "  --- build ${1}-dashboard "
./build-one-dashboard.sh ${1}
echo "  --- upload to grafana"
./upload_to_dev_grafana.py ${1}-dashboard.txt