#!/usr/bin/env python3
import os
print("token exists:", os.path.exists(os.path.expanduser("~/.hermes/google_token.json")))
print("token path:", os.path.expanduser("~/.hermes/google_token.json"))
try:
    import googleapiclient
    print("google-api-python-client version:", getattr(googleapiclient, "__version__", "unknown"))
except ImportError as e:
    print("google-api-python-client NOT available:", e)
