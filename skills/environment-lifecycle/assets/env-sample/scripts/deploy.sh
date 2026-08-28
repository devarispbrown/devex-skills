#!/usr/bin/env bash
set -euo pipefail

STAGE="${1:?usage: deploy.sh <stage>}"

echo "deploying app to ${STAGE}"

# Plain deploy: no lifecycle markers are set here, so environments created
# by this script are expected to persist until removed by hand.
