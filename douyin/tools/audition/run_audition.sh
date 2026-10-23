#!/bin/bash
set -e
cd ~/workspace/douyin/tools/audition
[ -d .venv ] || python3 -m venv .venv
. .venv/bin/activate
pip -q install "faster-whisper==1.1.0" "av==12.3.0" requests 2>&1 | tail -1
python3 audition.py
