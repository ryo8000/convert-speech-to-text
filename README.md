# convert-speech-to-text

This is a sample of converting speech data to text. This uses AWS services such as Amazon Transcribe.

When an audio file is placed in S3, a text file is generated based on the content of the audio file.

## Deploy

Deploy using terraform. Execute the following command.

```
terraform apply
```

Then enter your AWS account id and AWS S3 bucket.

Enter yes to the last question to deploy.
