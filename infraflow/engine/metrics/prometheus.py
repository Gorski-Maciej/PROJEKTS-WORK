try:
    from prometheus_client import Counter
except Exception:  # pragma: no cover
    class _Dummy:
        def labels(self, **kwargs):
            return self
        def inc(self, n: int = 1):
            return None
    def Counter(*args, **kwargs):
        return _Dummy()

INCIDENT_COUNTER = Counter('infraflow_incidents_total', 'Total incidents', ['server', 'priority'])
