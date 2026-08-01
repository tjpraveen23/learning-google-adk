from opentelemetry.sdk.trace.export import SpanExporter, SpanExportResult
from datetime import datetime

def format_time(ns: int) -> str:
        """Convert Unix nanoseconds to readable time."""
        return datetime.fromtimestamp(ns / 1_000_000_000).strftime("%H:%M:%S.%f")[:-3]

class SimpleConsoleExporter(SpanExporter):

    def export(self, spans):

        print("\n" + "=" * 70)
        print("TRACE")
        print("=" * 70)

        for span in spans:

            duration = (span.end_time - span.start_time) / 1_000_000

            print(f"Span      : {span.name}")
            print(f"Start     : {format_time(span.start_time)}")
            print(f"End       : {format_time(span.end_time)}")
            print(f"Duration  : {duration:.2f} ms")
            print("-" * 70)

        return SpanExportResult.SUCCESS