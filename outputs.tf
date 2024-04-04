output "lambda_transcriber" {
  value = aws_lambda_function.lambda_transcriber.qualified_arn
}
output "lambda_file_creator" {
  value = aws_lambda_function.lambda_file_creator.qualified_arn
}
