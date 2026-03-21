import gc
import logging
import threading

from fastapi import FastAPI
from opentelemetry import trace, metrics
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from sqlalchemy import Engine

from open_webui.utils.telemetry.exporters import LazyBatchSpanProcessor
from open_webui.utils.telemetry.instrumentors import Instrumentor
from open_webui.env import OTEL_SERVICE_NAME, OTEL_EXPORTER_OTLP_ENDPOINT

log = logging.getLogger(__name__)


def _setup_system_metrics(resource: Resource, endpoint: str):
    """Set up OTEL metrics with system-level gauges (CPU, memory, GC, threads)."""
    metric_reader = PeriodicExportingMetricReader(
        OTLPMetricExporter(endpoint=endpoint),
        export_interval_millis=30_000,
    )
    meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
    metrics.set_meter_provider(meter_provider)

    meter = metrics.get_meter("open_webui.system")

    # Try to import psutil; if unavailable, register only GC/thread metrics
    try:
        import psutil

        _process = psutil.Process()

        def _cpu_cb(_options):
            try:
                return [metrics.Observation(psutil.cpu_percent(interval=None))]
            except Exception:
                return []

        def _mem_rss_cb(_options):
            try:
                return [metrics.Observation(_process.memory_info().rss)]
            except Exception:
                return []

        def _mem_percent_cb(_options):
            try:
                return [metrics.Observation(psutil.virtual_memory().percent)]
            except Exception:
                return []

        meter.create_observable_gauge(
            name="system.cpu.percent",
            callbacks=[_cpu_cb],
            description="System CPU usage percent",
            unit="%",
        )
        meter.create_observable_gauge(
            name="process.memory.rss",
            callbacks=[_mem_rss_cb],
            description="Process resident set size in bytes",
            unit="By",
        )
        meter.create_observable_gauge(
            name="system.memory.percent",
            callbacks=[_mem_percent_cb],
            description="System memory usage percent",
            unit="%",
        )
    except ImportError:
        log.info("psutil not installed, skipping CPU/memory metrics")

    # GC collections
    def _gc_cb(_options):
        stats = gc.get_stats()
        observations = []
        for gen, s in enumerate(stats):
            observations.append(
                metrics.Observation(s["collections"], {"generation": str(gen)})
            )
        return observations

    meter.create_observable_gauge(
        name="runtime.python.gc.collections",
        callbacks=[_gc_cb],
        description="Python GC collection count per generation",
    )

    # Thread count
    def _thread_cb(_options):
        return [metrics.Observation(threading.active_count())]

    meter.create_observable_gauge(
        name="runtime.python.threads",
        callbacks=[_thread_cb],
        description="Active Python thread count",
    )


def setup(app: FastAPI, db_engine: Engine):
    resource = Resource.create(attributes={SERVICE_NAME: OTEL_SERVICE_NAME})

    # set up trace
    trace.set_tracer_provider(TracerProvider(resource=resource))
    # otlp export
    exporter = OTLPSpanExporter(endpoint=OTEL_EXPORTER_OTLP_ENDPOINT)
    trace.get_tracer_provider().add_span_processor(LazyBatchSpanProcessor(exporter))
    Instrumentor(app=app, db_engine=db_engine).instrument()

    # set up system metrics
    _setup_system_metrics(resource, OTEL_EXPORTER_OTLP_ENDPOINT)
