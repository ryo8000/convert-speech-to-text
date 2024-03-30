output "lambda_transcription" {
  value = aws_lambda_function.lambda_transcription.qualified_arn
}
output "lambda_file_creator" {
  value = aws_lambda_function.lambda_file_creator.qualified_arn
}
