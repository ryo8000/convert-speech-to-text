# convert-speech-to-text

This is a sample of converting speech data to text. This uses AWS services such as Amazon Transcribe.

When an audio file is placed in S3, a text file is generated based on the content of the audio file.

## Deploy

1. Deploy using terraform. Execute the following command.

```
terraform apply
```

2. Enter your AWS account id, AWS region and AWS S3 bucket.

3. Enter yes to the last question to deploy.

## Setup a development environment

1. Install VSCode and Docker.
2. Install the "Remote Development" extension for VSCode and open the workspace in dev container.

## Test

Open the workspace in the dev container, and Click on "Testing" in the activity bar.
