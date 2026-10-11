#!/bin/sh
# A shared/ forrásait a pluginokba másolja; --check esetén csak az eltérést jelzi.
set -e
cd "$(dirname "$0")/.."
status=0
for plugin in plugins/*/; do
  target="${plugin}scripts/harness_core.py"
  if [ "$1" = "--check" ]; then
    cmp -s shared/harness_core.py "$target" || { echo "Eltér: $target"; status=1; }
  else
    cp shared/harness_core.py "$target"
  fi
done
exit $status
