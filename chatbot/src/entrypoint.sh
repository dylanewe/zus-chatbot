#!/bin/bash

echo "Starting the chatbot service..."

uvicorn main:app --host 0.0.0.0 --port 8000 --reload