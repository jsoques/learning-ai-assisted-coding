#!/bin/bash
# Discover the Aspire dashboard OTLP API key and forward to Python process
# The dashboard process has DASHBOARD__OTLP__PRIMARYAPIKEY in its environ

DASHBOARD_PID=$(pgrep -f 'Aspire.Dashboard.dll$' 2>/dev/null | head -1)
if [ -n "$DASHBOARD_PID" ]; then
    OTLP_API_KEY=$(tr '\0' '\n' < "/proc/${DASHBOARD_PID}/environ" 2>/dev/null \
        | grep '^DASHBOARD__OTLP__PRIMARYAPIKEY=' \
        | cut -d= -f2)
    if [ -n "$OTLP_API_KEY" ]; then
        export OTEL_EXPORTER_OTLP_HEADERS="x-otlp-api-key=${OTLP_API_KEY}"
        echo "[otel_wrapper] Discovered OTLP API key" >&2
    fi
fi

export OTEL_EXPORTER_OTLP_ENDPOINT="http://localhost:19090"

exec "$@"
