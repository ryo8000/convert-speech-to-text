output "lambda_transcription" {
  value = aws_lambda_function.lambda_transcription.qualified_arn
}
output "lambda_creation" {
  value = aws_lambda_function.lambda_creation.qualified_arn
}
