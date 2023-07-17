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
