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

resource "aws_iam_role" "lambda_transcriber_role" {
  name                 = "${var.service_name}-transcriber-role"
  assume_role_policy   = data.aws_iam_policy_document.assume_role_policy.json
  description          = "Lambda role for ${var.service_name}-transcriber"
  max_session_duration = 3600
  path                 = "/"
  tags                 = {}
}

resource "aws_iam_role" "lambda_file_creator_role" {
  name                 = "${var.service_name}-file-creator-role"
  assume_role_policy   = data.aws_iam_policy_document.assume_role_policy.json
  description          = "Lambda role for ${var.service_name}-file-creator"
  max_session_duration = 3600
  path                 = "/"
  tags                 = {}
}

resource "aws_iam_role_policy" "lambda_transcriber_role_policy" {
  name = "${var.service_name}TranscriberPolicy"
  role = aws_iam_role.lambda_transcriber_role.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        "Sid" : "Statement0",
        "Effect" : "Allow",
        "Action" : [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents",
          "transcribe:StartTranscriptionJob"
        ],
        "Resource" : [
          "*"
        ]
      },
      {
        "Sid" : "Statement1",
        "Effect" : "Allow",
        "Action" : [
          "sqs:ReceiveMessage",
          "sqs:DeleteMessage",
          "sqs:GetQueueAttributes"
        ],
        "Resource" : ["${aws_sqs_queue.TranscriberQueue.arn}"]
      },
      {
        "Sid" : "Statement2",
        "Effect" : "Allow",
        "Action" : [
          "s3:*"
        ],
        "Resource" : [
          "arn:aws:s3:::${var.aws_s3_bucket}/*"
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy" "lambda_file_creator_role_policy" {
  name = "${var.service_name}FileCreatorPolicy"
  role = aws_iam_role.lambda_file_creator_role.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        "Sid" : "Statement0",
        "Effect" : "Allow",
        "Action" : [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents",
          "transcribe:DeleteTranscriptionJob",
        ],
        "Resource" : [
          "*"
        ]
      },
      {
        "Sid" : "Statement1",
        "Effect" : "Allow",
        "Action" : [
          "sqs:ReceiveMessage",
          "sqs:DeleteMessage",
          "sqs:GetQueueAttributes"
        ],
        "Resource" : ["${aws_sqs_queue.FileCreatorQueue.arn}"]
      },
      {
        "Sid" : "Statement2",
        "Effect" : "Allow",
        "Action" : [
          "s3:PutObject",
          "s3:GetObject"
        ],
        "Resource" : [
          "arn:aws:s3:::${var.aws_s3_bucket}/*"
        ]
      }
    ]
  })
}

# Lambda
resource "aws_lambda_function" "lambda_transcriber" {
  description = "create a transcription job."
  environment {
    variables = {
      AWS_S3_TRANSCRIPTION_DIST_KEY = var.aws_s3_transcription_dist_key
      AWS_S3_CREATION_DIST_KEY      = var.aws_s3_creation_dist_key
      AWS_TRANSCRIBE_LANGUAGE_CODE  = var.aws_transcribe_language_code
    }
  }
  function_name = "${var.service_name}-transcriber"
  handler       = "transcriber.lambda_handler"
  architectures = [
    "x86_64"
  ]
  filename         = data.archive_file.lambda_zip.output_path
  memory_size      = var.lambda_memory_size
  role             = aws_iam_role.lambda_transcriber_role.arn
  runtime          = var.lambda_runtime
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  timeout          = var.lambda_timeout
  tracing_config {
    mode = "PassThrough"
  }
}

resource "aws_lambda_function" "lambda_file_creator" {
  description = "create transcripts."
  environment {
    variables = {
      AWS_S3_TRANSCRIPTION_DIST_KEY = var.aws_s3_transcription_dist_key
      AWS_S3_CREATION_DIST_KEY      = var.aws_s3_creation_dist_key
      AWS_TRANSCRIBE_LANGUAGE_CODE  = var.aws_transcribe_language_code
    }
  }
  function_name = "${var.service_name}-file-creator"
  handler       = "file_creator.lambda_handler"
  architectures = [
    "x86_64"
  ]
  filename         = data.archive_file.lambda_zip.output_path
  memory_size      = var.lambda_memory_size
  role             = aws_iam_role.lambda_file_creator_role.arn
  runtime          = var.lambda_runtime
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  timeout          = var.lambda_timeout
  tracing_config {
    mode = "PassThrough"
  }
}

resource "aws_lambda_event_source_mapping" "LambdaTranscriberEventSourceMapping" {
  batch_size       = var.lambda_event_batch_size
  event_source_arn = aws_sqs_queue.TranscriberQueue.arn
  function_name    = aws_lambda_function.lambda_transcriber.arn
  enabled          = true
}

resource "aws_lambda_event_source_mapping" "lambdaFileCreatorEventSourceMapping" {
  batch_size       = var.lambda_event_batch_size
  event_source_arn = aws_sqs_queue.FileCreatorQueue.arn
  function_name    = aws_lambda_function.lambda_file_creator.arn
  enabled          = true
}

# SQS
resource "aws_sqs_queue" "TranscriberQueue" {
  delay_seconds              = var.sqs_delay_seconds
  max_message_size           = var.sqs_max_message_size
  message_retention_seconds  = var.sqs_message_retention_seconds
  receive_wait_time_seconds  = var.sqs_receive_wait_time_seconds
  visibility_timeout_seconds = var.sqs_visibility_timeout_seconds
  name                       = "${var.service_name}TranscriberQueue"
}

resource "aws_sqs_queue" "FileCreatorQueue" {
  delay_seconds              = var.sqs_delay_seconds
  max_message_size           = var.sqs_max_message_size
  message_retention_seconds  = var.sqs_message_retention_seconds
  receive_wait_time_seconds  = var.sqs_receive_wait_time_seconds
  visibility_timeout_seconds = var.sqs_visibility_timeout_seconds
  name                       = "${var.service_name}FileCreatorQueue"
}

data "aws_iam_policy_document" "TranscriberQueuePolicy" {
  statement {
    sid    = ""
    effect = "Allow"
    principals {
      identifiers = ["s3.amazonaws.com"]
      type        = "Service"
    }
    actions   = ["sqs:SendMessage"]
    resources = [aws_sqs_queue.TranscriberQueue.arn]
    condition {
      test     = "ArnLike"
      variable = "aws:SourceArn"
      values   = ["arn:aws:s3:::${var.aws_s3_bucket}"]
    }
  }
}

data "aws_iam_policy_document" "FileCreatorQueuePolicy" {
  statement {
    sid    = ""
    effect = "Allow"
    principals {
      identifiers = ["s3.amazonaws.com"]
      type        = "Service"
    }
    actions   = ["sqs:SendMessage"]
    resources = [aws_sqs_queue.FileCreatorQueue.arn]
    condition {
      test     = "ArnLike"
      variable = "aws:SourceArn"
      values   = ["arn:aws:s3:::${var.aws_s3_bucket}"]
    }
  }
}

resource "aws_sqs_queue_policy" "TranscriberQueuePolicy" {
  policy    = data.aws_iam_policy_document.TranscriberQueuePolicy.json
  queue_url = aws_sqs_queue.TranscriberQueue.id
}

resource "aws_sqs_queue_policy" "FileCreatorQueuePolicy" {
  policy    = data.aws_iam_policy_document.FileCreatorQueuePolicy.json
  queue_url = aws_sqs_queue.FileCreatorQueue.id
}
