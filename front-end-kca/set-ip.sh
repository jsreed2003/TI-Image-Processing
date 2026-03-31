#!/bin/sh
# Auto-detects the current machine's local IP and writes it to .env
IP=$(ipconfig getifaddr en0)
if [ -z "$IP" ]; then
  IP=$(ipconfig getifaddr en1)
fi
if [ -z "$IP" ]; then
  echo "Warning: Could not detect local IP. Falling back to localhost."
  IP="localhost"
fi
echo "VITE_API_URL=http://$IP:8000" > .env
echo "Set API URL to http://$IP:8000"
