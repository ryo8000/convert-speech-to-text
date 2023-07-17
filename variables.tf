variable "aws_region" {
  default     = "ap-northeast-1"
  description = "The AWS region to deploy products."
  type        = string
}

variable "service_name" {
  default     = "Transcribe"
  description = "service name"
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
