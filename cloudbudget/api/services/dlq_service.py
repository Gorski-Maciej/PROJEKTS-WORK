from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class DLQMessage:
    message_id: str
    queue: str
    payload: dict
    reason: str
    failed_at: str


class InMemoryDLQ:
    def __init__(self) -> None:
        self._messages: list[DLQMessage] = []

    def add(self, message_id: str, queue: str, payload: dict, reason: str) -> DLQMessage:
        item = DLQMessage(
            message_id=message_id,
            queue=queue,
            payload=payload,
            reason=reason,
            failed_at=datetime.now(timezone.utc).isoformat(),
        )
        self._messages.append(item)
        return item

    def list(self) -> list[dict]:
        return [m.__dict__ for m in self._messages]

    def requeue(self, message_id: str) -> dict:
        for i, msg in enumerate(self._messages):
            if msg.message_id == message_id:
                item = self._messages.pop(i)
                return {"status": "requeued", "message_id": item.message_id, "queue": item.queue}
        return {"status": "not_found", "message_id": message_id}


dlq_store = InMemoryDLQ()
