import configparser
import logging
import os
import pathlib
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
    textract_response = ''

    def __init__(self, access_key, secret_key,role, bucket, document, region,pdf_key):

        logging.basicConfig(filename=
         str(pathlib.Path(__file__).parent.resolve()) + '/log/log.log',
                    format='%(asctime)s %(message)s',
                    filemode='w')


        self.roleArn = role
        self.bucket = bucket
        self.document = document
        self.region_name = region
        self.access_key = access_key
        self.secret_key = secret_key
        self.pdf_key = pdf_key
        self.s3_pdf_location = self.pdf_key + str(os.path.basename(self.document))
        self.textract = boto3.client('textract',     
                    aws_access_key_id=self.access_key,aws_secret_access_key=self.secret_key,region_name=self.region_name
                    )

        self.s3 = boto3.client('s3',     
                    aws_access_key_id=self.access_key,aws_secret_access_key=self.secret_key,region_name=self.region_name
                    )

        self.sqs = boto3.client('sqs',aws_access_key_id=self.access_key,aws_secret_access_key=self.secret_key,region_name=self.region_name)
        self.sns = boto3.client('sns',aws_access_key_id=self.access_key,aws_secret_access_key=self.secret_key,region_name=self.region_name)

    def ProcessDocument(self):

        jobFound = False
        # print ( self.bucket,  self.document)
        self.textract_response = self.textract.start_document_analysis(DocumentLocation={'S3Object': {'Bucket': self.bucket, 'Name': self.s3_pdf_location}},
                FeatureTypes=["TABLES"], NotificationChannel={'RoleArn': self.roleArn, 'SNSTopicArn': self.snsTopicArn})

        with open(self.document, 'rb') as file:
            img_test = file.read()
            bytes_test = bytearray(img_test)
            # print('PDF loaded', self.document)

 
        # print('Processing type: Analysis')
        # print('Start Job Id: ' + response['JobId'])
        # print(self.textract_response['JobId'])

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

    
    def uploadFile(self):
        """Upload a file to an S3 bucket

        :param file_name: File to upload
        :param bucket: Bucket to upload to
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """
        # inside pdf folder 
        try:
            # Upload the file
            # s3_client.Object(self.bucket, s3_location).upload_file(self.document)
            self.s3.upload_file(Filename=self.document,Bucket=self.bucket,Key=self.s3_pdf_location)
            # with open(self.document, 'rb') as data:
            #     s3_client.upload_fileobj(data, self.bucket, s3_location)
        except Exception as e:
            logging.error(e.args)
            return False

        return True
        

def load_aws_config():
    config = configparser.ConfigParser()
    # print(str(pathlib.Path(__file__).parent.resolve()) + '/.aws/credentials')
    
    config.read( str(pathlib.Path(__file__).parent.resolve()) + '/.aws/credentials')
    aws_access_key_id = config.get("default","aws_access_key_id")
    aws_secret_access_key = config.get("default","aws_secret_access_key")
    region_name = config.get("default","region_name")
    role_arn = config.get("default","role_arn")
    bucket_name = config.get("s3","bucket")
    pdf_key = config.get("s3","pdf_key")
    return {"aws_access_key_id":aws_access_key_id, "aws_secret_access_key":aws_secret_access_key, "region_name":region_name, "role_arn":role_arn, "bucket_name":bucket_name, "pdf_key":pdf_key}

  
def main():
    
    document = sys.argv[1]     # document = 'pdf/AF_Dealer_Pricelist_072020_w.pdf'
    config = load_aws_config() # access_key, secret_key, region_name, role_arn
    
    roleArn = config["role_arn"]
    bucket = config["bucket_name"]
    
    region_name = config["region_name"]
    access_key = config["aws_access_key_id"]
    secret_key = config["aws_secret_access_key"]
    pdf_key = config["pdf_key"]

    # print(document)
    # print(config)
    
    analyzer = DocumentProcessor(access_key, secret_key,roleArn, bucket, document, region_name,pdf_key)
    if(analyzer.uploadFile()):
        analyzer.CreateTopicandQueue()
        analyzer.ProcessDocument()

if __name__ == "__main__":
    main()
