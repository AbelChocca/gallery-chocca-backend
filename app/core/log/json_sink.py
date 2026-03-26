import json
import sys
import traceback

def json_sink(message, stream=sys.stdout):
    record = message.record

    exc = record.get("exception")
    exc_text = None
    if exc:
        exc_text = "".join(
            traceback.format_exception(exc.type, exc.value, exc.traceback)
        )

    extra = record["extra"]

    payload = {
        "ts": record["time"].isoformat(),
        "level": record["level"].name,
        "message": record["message"],
        "logger": record["name"],
        "module": record["module"],
        "function": record["function"],
        "line": record["line"],
        **extra
    }
    if exc_text:
        lines = exc_text.splitlines()

        tail = "\n".join(lines[-20:])
        payload["exception_tail"] = tail

    print(json.dumps(payload, ensure_ascii=False), file=stream)