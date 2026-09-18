#!/usr/bin/env python3
"""Cron entrypoint wrapper for real CRM analytics report.
Uses the ops project's Google Sheets CRM (real data, no mock).
"""
import os
import sys

OPS_ROOT = os.path.expanduser("~/.hermes/ops")
sys.path.insert(0, OPS_ROOT)

from crm_real_report import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
