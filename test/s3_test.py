import os
import pathlib
import unittest

from start_doc_analysis_for_table_extraction import DocumentProcessor, load_aws_config

class TestS3(unittest.TestCase):

    def test_upload(self):
        document = './json/AF_Dealer_Pricelist_072020_w copy.json'     # document = 'pdf/AF_Dealer_Pricelist_072020_w.pdf'
        config = load_aws_config() # access_key, secret_key, region_name, role_arn
        
            
        roleArn = config["role_arn"]
        bucket = config["bucket_name"]
        
        region_name = config["region_name"]
        access_key = config["aws_access_key_id"]
        secret_key = config["aws_secret_access_key"]

        # print(document)
        # print(config)
        analyzer = DocumentProcessor(access_key, secret_key,roleArn, bucket, document, region_name)
        success = analyzer.uploadFile()
        self.assertTrue(success)
        
    
if __name__ == '__main__':
    unittest.main()
