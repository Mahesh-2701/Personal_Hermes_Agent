#!/usr/bin/env python3
try:
    import gspread
    print("gspread available, version:", getattr(gspread, '__version__', 'unknown'))
except ImportError as e:
    print("gspread NOT available:", e)

try:
    import google.auth
    print("google-auth available")
except ImportError as e:
    print("google-auth NOT available:", e)
