#!/usr/bin/env python3
"""Cron entrypoint wrapper for the Stage 4 morning brief workflow.

Keeps the real implementation in ~/.hermes/ops (the ops project, under git)
as the single source of truth. This wrapper only sets up sys.path and
delegates -- edit ~/.hermes/ops/workflows/morning_brief_report.py, not this
file, when changing behavior.
"""
import os
import sys

OPS_ROOT = os.path.expanduser("~/.hermes/ops")
sys.path.insert(0, OPS_ROOT)

from workflows.morning_brief_report import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
