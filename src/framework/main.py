from __future__ import annotations

import logging
import os
import sys

import uvicorn

from src.framework.db.session import engine
from src.framework.di.composition_root import create_app

app = create_app()

otlp_endpoint = os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT", "").strip()

if otlp_endpoint:
    from opentelemetry import _logs, metrics, trace
    from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
    from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
    from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
    from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
    from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
    from opentelemetry.sdk.metrics import MeterProvider
    from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
    from opentelemetry.sdk.resources import SERVICE_NAME, Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor

    logger = logging.getLogger("ecommerce.telemetry")
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
    logger.addHandler(handler)

    logger.info("OTLP endpoint: %s", otlp_endpoint)
    logger.info("OTLP headers: %s", os.environ.get("OTEL_EXPORTER_OTLP_HEADERS", "(not set)"))

    resource = Resource(attributes={SERVICE_NAME: "ecommerce-api"})

    channel_options = (
        ("grpc.http2.connection_type", "prior_knowledge"),
        ("grpc.connect_timeout_ms", 5000),
    )

    logger.info("Configuring trace provider...")
    try:
        span_exporter = OTLPSpanExporter(endpoint=otlp_endpoint, channel_options=channel_options)
        trace_provider = TracerProvider(resource=resource)
        trace_provider.add_span_processor(BatchSpanProcessor(span_exporter))
        trace.set_tracer_provider(trace_provider)
        FastAPIInstrumentor.instrument_app(app)
        SQLAlchemyInstrumentor().instrument(engine=engine)
        logger.info("Trace provider configured")
    except Exception as e:
        logger.error("Failed to configure trace provider: %s", e, exc_info=True)

    logger.info("Configuring metrics provider...")
    try:
        metric_exporter = OTLPMetricExporter(endpoint=otlp_endpoint, channel_options=channel_options)
        metric_reader = PeriodicExportingMetricReader(metric_exporter)
        meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
        metrics.set_meter_provider(meter_provider)
        logger.info("Metrics provider configured")
    except Exception as e:
        logger.error("Failed to configure metrics provider: %s", e, exc_info=True)

    logger.info("Configuring logs provider...")
    try:
        log_exporter = OTLPLogExporter(endpoint=otlp_endpoint, channel_options=channel_options)
        logger_provider = LoggerProvider(resource=resource)
        logger_provider.add_log_record_processor(BatchLogRecordProcessor(log_exporter))
        _logs.set_logger_provider(logger_provider)
        otel_handler = LoggingHandler(logger_provider=logger_provider)
        logging.getLogger().addHandler(otel_handler)
        logger.info("Logs provider configured")
    except Exception as e:
        logger.error("Failed to configure logs provider: %s", e, exc_info=True)

    logger.info("Creating test span...")
    try:
        tracer = trace.get_tracer(__name__)
        with tracer.start_as_current_span("startup-test") as span:
            span.set_attribute("test", "true")
        logger.info("Test span exported")
    except Exception as e:
        logger.error("Test span failed: %s", e, exc_info=True)

if __name__ == "__main__":
    uvicorn.run("src.framework.main:app", host="0.0.0.0", port=5566, reload=True)
