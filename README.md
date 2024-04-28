# convert-speech-to-text

This application converts speech data to text, using AWS services such as Amazon Transcribe.

When an audio file is placed in S3, a text file is generated based on the content of the audio file.

## Setup a development environment

1. Install VSCode, Docker and terraform.
2. Install the "Remote Development" extension for VSCode and open the workspace in dev container.

## Deploy

1. (First time only) Prepare one S3 bucket that this application is linked to.
2. (First time only) Execute the following command.
   ```
   pip3 install -r requirements.txt -t build/layers/transcribe/python
   ```
3. (First time only) Execute the following command.
   ```
   terraform init
   ```
4. Execute the following command.
   ```
   terraform apply
   ```
5. Enter values for each of the following items.
   - AWS account id: your AWS account ID
   - AWS S3 bucket: name of the S3 bucket you have prepared
   - AWS region: name of the region where this application is deployed. This must be the same as the region of the S3 bucket you have prepared
6. Enter 'yes' to the last question. Deployment is then performed.
7. (First time only) Open AWS console and go to the S3 page.
8. (First time only) Open the S3 bucket you have prepared and create two S3 event notifications.
   1. Audio file creation event
      - Event name: arbitrary value
      - Prefix: arbitrary S3 key name. Audio files created here are converted to text.
      - Event type: [ All object create events ]
      - Destination: SQS queue
      - SQS queue: transcribeTranscriberQueue
   2. Transcription file creation event
      - Event name: arbitrary value
      - Prefix: output/
      - Suffix: .json
      - Event type: [ All object create events ]
      - Destination: SQS queue
      - SQS queue: transcribeFileCreatorQueue

## Convert speech to text

Create an audio file in the S3 key created above. After a short time, the text file is output to output/ in S3.

## Test

Open the workspace in the dev container, and Click on "Testing" in the activity bar.
