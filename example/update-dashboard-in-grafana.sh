#!/bin/sh
echo "  --- build ${1}-dashboard "
./build-one-dashboard.sh ${1}
echo "  --- upload to grafana"
./create-dashboard-in-grafana.py ${1}-dashboard.txt
