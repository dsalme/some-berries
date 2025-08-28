#!/bin/bash

uv run uvicorn berries:app --host 0.0.0.0 --port 8000 --reload
