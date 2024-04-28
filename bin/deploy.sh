#!/bin/bash
set -e

terraform fmt
terraform apply
