terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  required_version = ">= 1.2.0"
}

provider "aws" {
  region = var.aws_region
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
  name               = "${var.service_name}-transcriber-role"
  assume_role_policy = data.aws_iam_policy_document.assume_role_policy.json
  description        = "Lambda role for ${var.service_name}-transcriber"
  tags = {
    Service = var.service_name
  }
}

resource "aws_iam_role" "lambda_file_creator_role" {
  name               = "${var.service_name}-file-creator-role"
  assume_role_policy = data.aws_iam_policy_document.assume_role_policy.json
  description        = "Lambda role for ${var.service_name}-file-creator"
  tags = {
    Service = var.service_name
  }
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
        "Resource" : ["${aws_sqs_queue.transcriber_queue.arn}"]
      },
      {
        "Sid" : "Statement2",
        "Effect" : "Allow",
        "Action" : [
          "s3:GetObject",
          "s3:PutObject"
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
        "Resource" : ["${aws_sqs_queue.file_creator_queue.arn}"]
      },
      {
        "Sid" : "Statement2",
        "Effect" : "Allow",
        "Action" : [
          "s3:GetObject",
          "s3:PutObject"
        ],
        "Resource" : [
          "arn:aws:s3:::${var.aws_s3_bucket}/*"
        ]
      }
    ]
  })
}

# Lambda
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "src"
  output_path = "lambda_function_payload.zip"
}

resource "aws_lambda_function" "lambda_transcriber" {
  description = "create a transcription job."
  environment {
    variables = {
      AWS_S3_TRANSCRIPTION_DIST_KEY = var.aws_s3_transcription_dist_key
      AWS_S3_CREATION_DIST_KEY      = var.aws_s3_creation_dist_key
      AWS_TRANSCRIBE_LANGUAGE_CODE  = var.aws_transcribe_language_code
    }
  }
  filename         = "lambda_function_payload.zip"
  function_name    = "${var.service_name}-transcriber"
  handler          = "transcriber.lambda_handler"
  memory_size      = var.lambda_memory_size
  role             = aws_iam_role.lambda_transcriber_role.arn
  runtime          = var.lambda_runtime
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  timeout          = var.lambda_timeout
  tags = {
    Service = var.service_name
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
  filename         = "lambda_function_payload.zip"
  function_name    = "${var.service_name}-file-creator"
  handler          = "file_creator.lambda_handler"
  memory_size      = var.lambda_memory_size
  role             = aws_iam_role.lambda_file_creator_role.arn
  runtime          = var.lambda_runtime
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  timeout          = var.lambda_timeout
  tags = {
    Service = var.service_name
  }
}

resource "aws_lambda_event_source_mapping" "lambda_transcriber_event_source_mapping" {
  batch_size       = var.lambda_event_batch_size
  event_source_arn = aws_sqs_queue.transcriber_queue.arn
  function_name    = aws_lambda_function.lambda_transcriber.arn
}

resource "aws_lambda_event_source_mapping" "lambda_file_creator_event_source_mapping" {
  batch_size       = var.lambda_event_batch_size
  event_source_arn = aws_sqs_queue.file_creator_queue.arn
  function_name    = aws_lambda_function.lambda_file_creator.arn
}

# SQS
resource "aws_sqs_queue" "transcriber_queue" {
  name                       = "${var.service_name}TranscriberQueue"
  delay_seconds              = var.sqs_delay_seconds
  max_message_size           = var.sqs_max_message_size
  message_retention_seconds  = var.sqs_message_retention_seconds
  receive_wait_time_seconds  = var.sqs_receive_wait_time_seconds
  visibility_timeout_seconds = var.sqs_visibility_timeout_seconds
  tags = {
    Service = var.service_name
  }
}

resource "aws_sqs_queue" "file_creator_queue" {
  name                       = "${var.service_name}FileCreatorQueue"
  delay_seconds              = var.sqs_delay_seconds
  max_message_size           = var.sqs_max_message_size
  message_retention_seconds  = var.sqs_message_retention_seconds
  receive_wait_time_seconds  = var.sqs_receive_wait_time_seconds
  visibility_timeout_seconds = var.sqs_visibility_timeout_seconds
  tags = {
    Service = var.service_name
  }
}

data "aws_iam_policy_document" "transcriber_queue_policy" {
  statement {
    sid    = ""
    effect = "Allow"
    principals {
      identifiers = ["s3.amazonaws.com"]
      type        = "Service"
    }
    actions   = ["sqs:SendMessage"]
    resources = [aws_sqs_queue.transcriber_queue.arn]
    condition {
      test     = "ArnLike"
      variable = "aws:SourceArn"
      values   = ["arn:aws:s3:::${var.aws_s3_bucket}"]
    }
  }
}

data "aws_iam_policy_document" "file_creator_queue_policy" {
  statement {
    sid    = ""
    effect = "Allow"
    principals {
      identifiers = ["s3.amazonaws.com"]
      type        = "Service"
    }
    actions   = ["sqs:SendMessage"]
    resources = [aws_sqs_queue.file_creator_queue.arn]
    condition {
      test     = "ArnLike"
      variable = "aws:SourceArn"
      values   = ["arn:aws:s3:::${var.aws_s3_bucket}"]
    }
  }
}

resource "aws_sqs_queue_policy" "transcriber_queue_policy" {
  queue_url = aws_sqs_queue.transcriber_queue.id
  policy    = data.aws_iam_policy_document.transcriber_queue_policy.json
}

resource "aws_sqs_queue_policy" "file_creator_queue_policy" {
  queue_url = aws_sqs_queue.file_creator_queue.id
  policy    = data.aws_iam_policy_document.file_creator_queue_policy.json
}
