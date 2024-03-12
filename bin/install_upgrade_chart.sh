#!/bin/bash

release="jobberwocky"
namespace="avature"
secrets_name="${release}-secrets"
chart_dir="chart"

function check_command() {
  local cmd="$1"

  if ! command -v $cmd &>/dev/null; then
    echo "$cmd is not installed!"
    exit 1
  fi
}

if ! helm lint $chart_dir; then
  echo "Helm chart validation failed. Aborting."
  exit 1
fi

check_command helm
check_command kubectl

if ! kubectl get namespace $namespace &>/dev/null; then
  echo "Creating namespace ${namespace}..."
  kubectl create namespace $namespace
fi

if ! kubectl get secrets $secrets_name -n $namespace &>/dev/null; then
  echo
  echo "Creating secrets ${secrets_name}..."
  kubectl create secret generic $secrets_name \
    --namespace $namespace \
    --from-literal=jobberwocky_mailgun_domain="$JOBBERWOCKY_MAILGUN_DOMAIN" \
    --from-literal=jobberwocky_mailgun_api_key="$JOBBERWOCKY_MAILGUN_API_KEY"
fi

if ! helm status $release --namespace $namespace &>/dev/null; then
  echo
  echo "Installing chart ${release} into namespace ${namespace}..."
  helm install $release $chart_dir --namespace $namespace
else
  echo
  echo "Upgrading chart ${release} for namespace ${namespace}..."
  helm upgrade --cleanup-on-fail $release $chart_dir --namespace $namespace
fi

sleep 1
echo
echo "Helm releases for namespace ${namespace}"
helm list --namespace $namespace

sleep 1
echo
echo "Resources in namespace ${namespace}"
kubectl get all --namespace $namespace
