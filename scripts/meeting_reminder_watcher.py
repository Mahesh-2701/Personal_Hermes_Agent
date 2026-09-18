#!/usr/bin/env python3
"""Cron entrypoint wrapper for the Stage 15 meeting reminder watcher.

Keeps the real implementation in ~/.hermes/ops (the ops project, under git)
as the single source of truth. This wrapper only sets up sys.path and
delegates -- edit ~/.hermes/ops/workflows/meeting_reminder_watcher.py, not
this file, when changing behavior.
"""
import os
import sys

OPS_ROOT = os.path.expanduser("~/.hermes/ops")
sys.path.insert(0, OPS_ROOT)

from workflows.meeting_reminder_watcher import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
