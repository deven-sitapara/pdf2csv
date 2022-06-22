
import configparser
import os
import sys
import time
from get_doc_analysis_for_table_extraction import GetResults

from start_doc_analysis_for_table_extraction import DocumentProcessor, load_aws_config


def main():
    document = sys.argv[1]     # document = 'pdf/AF_Dealer_Pricelist_072020_w.pdf'
    csv_output = sys.argv[2]     # document = 'pdf/AF_Dealer_Pricelist_072020_w.pdf'
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
        
        jobId = analyzer.textract_response['JobId']
        counter = 0
        while True:

            if(counter > 30): 
                break            

            textract_response = (analyzer.textract.get_document_analysis(JobId=jobId))
            if(textract_response["JobStatus"] == "SUCCEEDED"):
                response_blocks = GetResults(analyzer.textract, jobId, csv_output)
                break
            elif(textract_response["JobStatus"] == "FAILED"):
                textract_response["JobStatus"]
                break
            
            # print(textract_response["JobStatus"])

            # sleep 3 seconds 
            time.sleep(3)     

            ++counter


if __name__ == "__main__":
    main()

# process_pdf.py source/pdf output_file/csv

