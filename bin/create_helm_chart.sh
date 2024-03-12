#!/bin/bash

chart_dir="chart"

echo "Verifying the chart..."
if ! helm lint $chart_dir; then
  echo "Helm chart validation failed. Aborting."
else
  echo
  echo "Packing the chart..."
  helm package $chart_dir
fi
