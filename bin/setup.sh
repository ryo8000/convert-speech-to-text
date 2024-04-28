#!/bin/bash
set -e

pip3 install -r requirements.txt -t build/layers/transcribe/python
terraform init
