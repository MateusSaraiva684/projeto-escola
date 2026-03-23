#!/usr/bin/env bash

echo "RODANDO START.SH CERTO 🔥"

uvicorn main:app --host 0.0.0.0 --port $PORT --reload