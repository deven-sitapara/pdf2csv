import configparser
import os


def main():
    config = configparser.ConfigParser()
    config.read('./.aws/credentials')
    aws_access_key_id = config.get("default","aws_access_key_id")
    aws_secret_access_key = config.get("default","aws_secret_access_key")
    region_name = config.get("default","region_name")
    print(aws_access_key_id , aws_secret_access_key , region_name)


if __name__ == "__main__":
    main()



