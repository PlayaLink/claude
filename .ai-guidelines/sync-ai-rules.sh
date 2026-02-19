#!/bin/bash
# Backward compatibility shim. Use ./.ai-guidelines/sync.sh
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "$SCRIPT_DIR/sync.sh" "$@"
