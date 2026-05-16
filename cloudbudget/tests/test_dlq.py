from api.services.dlq_service import InMemoryDLQ


def test_dlq_add_list_requeue():
    dlq = InMemoryDLQ()
    dlq.add("m1", "cost.ingest", {"x": 1}, "parse_error")
    dlq.add("m2", "cost.analyze", {"y": 2}, "timeout")
    assert len(dlq.list()) == 2

    result = dlq.requeue("m1")
    assert result["status"] == "requeued"
    assert len(dlq.list()) == 1
