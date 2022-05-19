# pdf to csv

## Extract table and convert to csv

```
    # Works
    # ------------------------------
    # ./venv/Scripts/python ./pdf2csv.py ./pdf/table.pdf
    # ./venv/Scripts/python ./pdf2csv.py ./pdf/Audinate\ -\ DVS\ and\ Via\ Reseller\ Pricing\ -\ January\ 6\,\ 2020.pdf

    # NOT WORKING
    # ------------------------------
    # ./venv/Scripts/python ./pdf2csv.py ./pdf/Roland\ Pro\ Reseller\ \(AVR\)\ Price\ List\ -\ April\ 1\,\ 2020.pdf
    # Image loaded ./pdf/Roland Pro Reseller (AVR) Price List - April 1, 2020.pdf
    # Traceback (most recent call last):
    #   File "D:\laragon\www\gkb_req\pricedonkey\pdf2csv\pdf2csv.py", line 118, in <module>
    #     main(file_name)
    #   File "D:\laragon\www\gkb_req\pricedonkey\pdf2csv\pdf2csv.py", line 104, in main
    #     table_csv = get_table_csv_results(file_name)
    #   File "D:\laragon\www\gkb_req\pricedonkey\pdf2csv\pdf2csv.py", line 63, in get_table_csv_results
    #     response = client.analyze_document(Document={'Bytes': bytes_test}, FeatureTypes=['TABLES'])
    #   File "D:\laragon\www\gkb_req\pricedonkey\pdf2csv\venv\lib\site-packages\botocore\client.py", line 415, in _api_call
    #     return self._make_api_call(operation_name, kwargs)
    #   File "D:\laragon\www\gkb_req\pricedonkey\pdf2csv\venv\lib\site-packages\botocore\client.py", line 745, in _make_api_call
    #     raise error_class(parsed_response, operation_name)
    # botocore.errorfactory.UnsupportedDocumentException: An error occurred (UnsupportedDocumentException) when calling the AnalyzeDocument operation: Request has unsupported document format
```
