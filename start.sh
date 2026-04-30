#!/bin/bash
# Seed the database (safe to run multiple times — skips if already seeded)
python seed.py
# Start the server
uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
