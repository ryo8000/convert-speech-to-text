terraform {
  required_version = ">= 0.12"
}

provider "aws" {
  region = var.aws_region
}

provider "archive" {}

data "archive_file" "lambda_zip" {
  type        = "zip"
  output_path = "src.zip"
  source_dir  = "src"
}

# IAM
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
  name                 = "${var.service_name}-role"
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

# API Gateway
resource "aws_api_gateway_rest_api" "rest_api" {
  name           = "${var.service_name}-rest-api"
  description    = "transcribe API of Transcribe service."
  api_key_source = "HEADER"
  endpoint_configuration {
    types = [
      "REGIONAL"
    ]
  }
  tags = {}
}

resource "aws_api_gateway_resource" "transcribe" {
  path_part   = "transcribe"
  parent_id   = aws_api_gateway_rest_api.rest_api.root_resource_id
  rest_api_id = aws_api_gateway_rest_api.rest_api.id
}

resource "aws_api_gateway_method" "get" {
  http_method      = "POST"
  authorization    = "NONE"
  api_key_required = false
  rest_api_id      = aws_api_gateway_rest_api.rest_api.id
  resource_id      = aws_api_gateway_resource.transcribe.id
}

resource "aws_api_gateway_integration" "integration" {
  rest_api_id             = aws_api_gateway_rest_api.rest_api.id
  resource_id             = aws_api_gateway_resource.transcribe.id
  http_method             = aws_api_gateway_method.get.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.lambda_transcriber.invoke_arn
}

resource "aws_api_gateway_deployment" "deployment" {
  description = "Created by terraform."
  rest_api_id = aws_api_gateway_rest_api.rest_api.id

  triggers = {
    # NOTE: The configuration below will satisfy ordering considerations,
    #       but not pick up all future REST API changes. More advanced patterns
    #       are possible, such as using the filesha1() function against the
    #       Terraform configuration file(s) or removing the .id references to
    #       calculate a hash against whole resources. Be aware that using whole
    #       resources will show a difference after the initial implementation.
    #       It will stabilize to only change when resources change afterwards.
    redeployment = sha1(jsonencode([
      aws_api_gateway_resource.transcribe.id,
      aws_api_gateway_method.get.id,
      aws_api_gateway_integration.integration.id,
    ]))
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_stage" "stage" {
  stage_name    = "api"
  rest_api_id   = aws_api_gateway_rest_api.rest_api.id
  deployment_id = aws_api_gateway_deployment.deployment.id
}

# Lambda
resource "aws_lambda_function" "lambda_transcriber" {
  description = "start a transcription job."
  environment {
    variables = {
      AWS_S3_REGION   = var.aws_region
      AWS_S3_BUCKET   = var.aws_s3_bucket
      AWS_S3_SRC_DIR  = var.aws_s3_src_dir
      AWS_S3_DIST_DIR = var.aws_s3_dist_dir
    }
  }
  function_name = "${var.service_name}-transcriber"
  handler       = "transcriber.lambda_handler"
  architectures = [
    "x86_64"
  ]
  filename         = data.archive_file.lambda_zip.output_path
  memory_size      = var.lambda_memory_size
  role             = aws_iam_role.lambda_role.arn
  runtime          = var.lambda_runtime
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  timeout          = var.lambda_timeout
  tracing_config {
    mode = "PassThrough"
  }
}

resource "aws_lambda_permission" "lambda_transcriber_permission" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_transcriber.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "arn:aws:execute-api:${var.aws_region}:${var.aws_account_id}:${aws_api_gateway_rest_api.rest_api.id}/*/${aws_api_gateway_method.get.http_method}${aws_api_gateway_resource.transcribe.path}"
}
