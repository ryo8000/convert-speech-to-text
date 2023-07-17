terraform {
  required_version = ">= 0.12"
}

provider "aws" {
  region = var.aws_region
}

provider "archive" {}

data "archive_file" "zip" {
  type        = "zip"
  output_path = "src.zip"
  source_dir  = "src"
}

data "aws_iam_policy_document" "policy" {
  statement {
    sid    = ""
    effect = "Allow"

    principals {
      identifiers = ["lambda.amazonaws.com"]
      type        = "Service"
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "lambda_role" {
  name               = "TranscribeRole"
  assume_role_policy = data.aws_iam_policy_document.policy.json
}

resource "aws_lambda_function" "lambda" {
  description = ""
  environment {
    variables = {
    }
  }
  filename      = data.archive_file.zip.output_path
  function_name = "hello-lambda"
  handler       = "hello_lambda.lambda_handler"
  architectures = [
    "x86_64"
  ]
  source_code_hash = data.archive_file.zip.output_base64sha256
  memory_size      = 128
  role             = aws_iam_role.lambda_role.arn
  runtime          = "python3.10"
  timeout          = 3
  tracing_config {
    mode = "PassThrough"
  }
}
