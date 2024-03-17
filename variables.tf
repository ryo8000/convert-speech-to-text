variable "service_name" {
  default     = "transcribe"
  description = "service name"
  type        = string
}

variable "aws_account_id" {
  description = "AWS account id"
  type        = string
}

variable "aws_region" {
  default     = "ap-northeast-1"
  description = "AWS region to deploy products."
  type        = string
}

variable "aws_s3_bucket" {
  description = "AWS S3 src bucket"
  type        = string
}

variable "aws_s3_src_dir" {
  default     = "input"
  description = "AWS S3 src dir"
  type        = string
}

variable "aws_s3_dist_dir" {
  default     = "output"
  description = "AWS S3 dist dir"
  type        = string
}

variable "lambda_memory_size" {
  default     = 128
  description = "lambda memory size"
  type        = number
}

variable "lambda_runtime" {
  default     = "python3.10"
  description = "lambda runtime"
  type        = string
}

variable "lambda_timeout" {
  default     = 5
  description = "lambda runtime"
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
