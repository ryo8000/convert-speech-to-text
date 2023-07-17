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

data "aws_iam_policy_document" "assume_role_policy" {
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

data "aws_partition" "current" {}

data "aws_iam_policy" "aws_lambda_basic_execution_role" {
  arn = "arn:${data.aws_partition.current.partition}:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

data "aws_iam_policy" "amazon_transcribe_full_access" {
  arn = "arn:${data.aws_partition.current.partition}:iam::aws:policy/AmazonTranscribeFullAccess"
}

data "aws_iam_policy" "amazon_s3_full_access" {
  arn = "arn:${data.aws_partition.current.partition}:iam::aws:policy/AmazonS3FullAccess"
}

resource "aws_iam_role" "lambda_role" {
  name                 = "${var.service_name}Role"
  assume_role_policy   = data.aws_iam_policy_document.assume_role_policy.json
  description          = "only for Transcribe"
  max_session_duration = 3600
  path                 = "/"
  tags                 = {}
}

resource "aws_iam_role_policy_attachment" "aws_lambda_basic_execution_role_attach" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = data.aws_iam_policy.aws_lambda_basic_execution_role.arn
}

resource "aws_iam_role_policy_attachment" "amazon_transcribe_full_access_attach" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = data.aws_iam_policy.amazon_transcribe_full_access.arn
}

resource "aws_iam_role_policy_attachment" "amazon_s3_full_access_attach" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = data.aws_iam_policy.amazon_s3_full_access.arn
}

resource "aws_lambda_function" "lambda_transcriber" {
  description = "start a transcription job."
  environment {
    variables = {
    }
  }
  function_name = "${var.service_name}-transcriber"
  handler       = "transcriber.lambda_handler"
  architectures = [
    "x86_64"
  ]
  filename         = data.archive_file.zip.output_path
  memory_size      = var.lambda_memory_size
  role             = aws_iam_role.lambda_role.arn
  runtime          = var.lambda_runtime
  source_code_hash = data.archive_file.zip.output_base64sha256
  timeout          = var.lambda_timeout
  tracing_config {
    mode = "PassThrough"
  }
}
