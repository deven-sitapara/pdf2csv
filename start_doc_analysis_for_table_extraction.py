import configparser
import sys
import boto3
import time

class DocumentProcessor:

    jobId = ''
    region_name = ''

    roleArn = ''
    bucket = ''
    document = ''

    sqsQueueUrl = ''
    snsTopicArn = ''
    processType = ''
    request_id = ''

    def __init__(self, access_key, secret_key,role, bucket, document, region):
        self.roleArn = role
        self.bucket = bucket
        self.document = document
        self.region_name = region
        self.access_key = access_key
        self.secret_key = secret_key
 
        self.textract = boto3.client('textract',     
                    aws_access_key_id=self.access_key,aws_secret_access_key=self.secret_key,region_name=self.region_name
                    )

        self.sqs = boto3.client('sqs',aws_access_key_id=self.access_key,aws_secret_access_key=self.secret_key,region_name=self.region_name)
        self.sns = boto3.client('sns',aws_access_key_id=self.access_key,aws_secret_access_key=self.secret_key,region_name=self.region_name)

    def ProcessDocument(self):

        jobFound = False
        # print ( self.bucket,  self.document)
        response = self.textract.start_document_analysis(DocumentLocation={'S3Object': {'Bucket': self.bucket, 'Name': self.document}},
                FeatureTypes=["TABLES"], NotificationChannel={'RoleArn': self.roleArn, 'SNSTopicArn': self.snsTopicArn})

        with open(self.document, 'rb') as file:
            img_test = file.read()
            bytes_test = bytearray(img_test)
            # print('PDF loaded', self.document)

 
        # print('Processing type: Analysis')
        # print('Start Job Id: ' + response['JobId'])
        print(response['JobId'])

        # print('Done!')

    def CreateTopicandQueue(self):

        millis = str(int(round(time.time() * 1000)))

        # Create SNS topic
        snsTopicName = "AmazonTextractTopic" + millis

        topicResponse = self.sns.create_topic(Name=snsTopicName)
        self.snsTopicArn = topicResponse['TopicArn']

        # create SQS queue
        sqsQueueName = "AmazonTextractQueue" + millis
        self.sqs.create_queue(QueueName=sqsQueueName)
        self.sqsQueueUrl = self.sqs.get_queue_url(QueueName=sqsQueueName)['QueueUrl']

        attribs = self.sqs.get_queue_attributes(QueueUrl=self.sqsQueueUrl, AttributeNames=['QueueArn'])['Attributes']
        sqsQueueArn = attribs['QueueArn']

        # Subscribe SQS queue to SNS topic
        self.sns.subscribe(TopicArn=self.snsTopicArn, Protocol='sqs', Endpoint=sqsQueueArn)

        # Authorize SNS to write SQS queue
        policy = """{{
                "Version":"2012-10-17",
                "Statement":[
                  {{
                    "Sid":"MyPolicy",
                    "Effect":"Allow",
                    "Principal" : {{"AWS" : "*"}},
                    "Action":"SQS:SendMessage",
                    "Resource": "{}",
                    "Condition":{{
                      "ArnEquals":{{
                        "aws:SourceArn": "{}"
                      }}
                    }}
                  }}
                ]
              }}""".format(sqsQueueArn, self.snsTopicArn)

        response = self.sqs.set_queue_attributes(
            QueueUrl=self.sqsQueueUrl,
            Attributes={
                'Policy': policy
            })
        self.request_id = response["ResponseMetadata"]["RequestId"]
        # print(self.request_id)
        # print(response)

def load_aws_config():
    config = configparser.ConfigParser()
    config.read('./.aws/credentials')
    aws_access_key_id = config.get("default","aws_access_key_id")
    aws_secret_access_key = config.get("default","aws_secret_access_key")
    region_name = config.get("default","region_name")
    role_arn = config.get("default","role_arn")
    bucket_name = config.get("s3","bucket")
    return {"aws_access_key_id":aws_access_key_id, "aws_secret_access_key":aws_secret_access_key, "region_name":region_name, "role_arn":role_arn, "bucket_name":bucket_name}


def main():
    
    document = sys.argv[1]     # document = 'pdf/AF_Dealer_Pricelist_072020_w.pdf'
    config = load_aws_config() # access_key, secret_key, region_name, role_arn
    
    roleArn = config["role_arn"]
    bucket = config["bucket_name"]
    
    region_name = config["region_name"]
    access_key = config["aws_access_key_id"]
    secret_key = config["aws_secret_access_key"]

    # print(document)
    # print(config)
    
    analyzer = DocumentProcessor(access_key, secret_key,roleArn, bucket, document, region_name)
    analyzer.CreateTopicandQueue()
    analyzer.ProcessDocument()

if __name__ == "__main__":
    main()
