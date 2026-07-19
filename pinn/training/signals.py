"""Main-thread signal helpers for the training composition root.

``on_escalate`` must only flush handlers and make one best-effort atomic status
update. It must not finalize summaries or checkpoint: both operations can acquire
locks or perform lengthy I/O while the main thread is interrupted.
"""

from __future__ import annotations

import os
import signal
import time
from dataclasses import dataclass
from typing import Callable, Optional


@dataclass
class SignalState:
    """Mutable signal state read by the training-loop stop seam."""

    first_signal_monotonic: Optional[float] = None
    stop_requested: bool = False
    escalate: bool = False
    exit_code: int = 130
    debounce_secs: float = 1.0


def note_signal(state: SignalState, now_monotonic: float) -> str:
    """Record SIGINT timing and return the required graceful/escalate action."""

    first = state.first_signal_monotonic
    if first is None:
        state.first_signal_monotonic = float(now_monotonic)
        state.stop_requested = True
        return "graceful"
    if float(now_monotonic) - first <= state.debounce_secs:
        state.stop_requested = True
        return "graceful"
    state.escalate = True
    return "escalate"


def install_signal_handlers(
    state: SignalState,
    on_escalate: Optional[Callable[[], None]] = None,
) -> Callable[[], None]:
    """Install SIGINT/SIGTERM handlers and return a callable restoring prior ones.

    Call only from ``pinn.train.main()`` on the main thread. The SIGINT escalation
    branch runs synchronously because the main loop might be stuck inside an
    optimizer step. SIGTERM is always a graceful stop request.
    """

    prev_int = signal.getsignal(signal.SIGINT)
    prev_term = signal.getsignal(signal.SIGTERM)

    def handle_sigint(_signum: int, _frame: object) -> None:
        state.exit_code = 130
        if note_signal(state, time.monotonic()) == "graceful":
            return
        if on_escalate is not None:
            try:
                on_escalate()
            except Exception:
                pass
        os._exit(130)

    def handle_sigterm(_signum: int, _frame: object) -> None:
        state.exit_code = 143
        state.stop_requested = True
        if state.first_signal_monotonic is None:
            state.first_signal_monotonic = time.monotonic()

    signal.signal(signal.SIGINT, handle_sigint)
    signal.signal(signal.SIGTERM, handle_sigterm)

    def restore() -> None:
        signal.signal(signal.SIGINT, prev_int)
        signal.signal(signal.SIGTERM, prev_term)

    return restore
