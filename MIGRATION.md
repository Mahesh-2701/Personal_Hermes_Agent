# Migration Guide

To migrate Hermes to a new machine:

1. **Clone the repository:**
   `git clone https://github.com/Mahesh-2701/hermes-agent-setup.git`

2. **Install prerequisites:**
   - Install Node.js (v20+)
   - Install Python 3.11+
   - Install Git

3. **Configure Environment:**
   - Copy `.env.example` to `.env`
   - Populate credentials (API keys, GitHub PAT)

4. **Initialize Hermes:**
   - Run `scripts/setup/bootstrap.sh` (or `.ps1`)

5. **Verify:**
   - Run `scripts/verify/verify-installation.sh`
