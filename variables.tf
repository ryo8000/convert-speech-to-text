variable "service_name" {
  default     = "transcribe"
  description = "this service name"
  type        = string
}

variable "aws_account_id" {
  description = "AWS account id"
  type        = string
}

variable "aws_s3_bucket" {
  description = "AWS S3 bucket"
  type        = string
}

variable "aws_region" {
  description = "AWS region to deploy products."
  type        = string
}

variable "aws_s3_transcription_dist_key" {
  default     = "output"
  description = "AWS S3 transcription dist key"
  type        = string
}

variable "aws_s3_creation_dist_key" {
  default     = "output"
  description = "AWS S3 creation dist key"
  type        = string
}

variable "aws_transcribe_language_code" {
  default     = "ja-JP"
  description = "language_code"
  type        = string
}

variable "lambda_log_level" {
  default     = "INFO"
  description = "lambda log level"
  type        = string
}

variable "lambda_memory_size" {
  default     = 128
  description = "lambda memory size"
  type        = number
}

variable "lambda_runtime" {
  default     = "python3.12"
  description = "lambda runtime"
  type        = string
}

variable "lambda_timeout" {
  default     = 5
  description = "lambda timeout"
  type        = number
}

variable "lambda_event_batch_size" {
  default     = 10
  description = "lambda event batch size"
  type        = number
}

variable "sqs_delay_seconds" {
  default     = 0
  description = "sqs delay seconds"
  type        = number
}

variable "sqs_max_message_size" {
  default     = 262144
  description = "sqs max message size"
  type        = number
}

variable "sqs_message_retention_seconds" {
  default     = 345600
  description = "sqs message retention seconds"
  type        = number
}

variable "sqs_receive_wait_time_seconds" {
  default     = 0
  description = "sqs receive wait time seconds"
  type        = number
}

variable "sqs_visibility_timeout_seconds" {
  default     = 30
  description = "sqs visibility timeout seconds"
  type        = number
}
