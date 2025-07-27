from dataclasses import dataclass, field
from typing import List, Dict
import time

@dataclass
class Command:
    ts: float
    cmd: str
    args: Dict

@dataclass
class CommandBuffer:
    buf: List[Command] = field(default_factory=list)

    def push(self, cmd: str, args: Dict = None):
        self.buf.append(Command(time.time(), cmd, args or {}))

    def as_rows(self):
        return [
            {"time": c.ts, "cmd": c.cmd, "args": str(c.args)}
            for c in self.buf
        ]
