import boto3 
import requests
import json

AWS_ACCESS_KEY = ''
AWS_SECRET_ACCESS_KEY =''

s3_client_connection = boto3.resource(
    's3',
    aws_access_key_id = AWS_ACCESS_KEY,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY
)

def check_grant(grant, bucket_name, key=''):

    #http://docs.aws.amazon.com/AmazonS3/latest/dev/acl-overview.html
    if grant['Grantee']['Type'].lower() == 'group' \
       and grant['Grantee']['URI'] == 'http://acs.amazonaws.com/groups/global/AllUsers':

        grant_permission = grant['Permission'].lower()
        granted_warning = 'The following permission: {} has been granted on s3://{}/{}'
        
        if grant_permission == 'read':
            return granted_warning.format('Read - Public Access: Read Object(s)', bucket_name, key), True
        elif grant_permission == 'write':
            return granted_warning.format('Write - Public Access: Write Object(s)', bucket_name, key), True
        elif grant_permission == 'read_acp':
            return granted_warning.format('Write - Public Access: Read Bucket Permission(s)', bucket_name, key), True
        elif grant_permission == 'write_acp':
            return granted_warning.format('Write - Public Access: Write Bucket Permission(s)', bucket_name, key), True
        elif grant_permission == 'full_control':
            return granted_warning.format('Public Access: Full Control', bucket_name, key), True

    return '', False

def check_S3_grants():
    for bucket in s3_client_connection.buckets.all():
        print(bucket.name)
        for grant in bucket.Acl().grants:
            warning, print_warning = check_grant(grant, bucket.name)
            if print_warning:            
                print warning

         # Look at acls for all objects in bucket       
        for obj in bucket.objects.all():
            for grant in obj.Acl().grants:
                warning, print_warning = check_grant(grant, bucket.name, obj.key)
                if print_warning:
                    print warning
                      
if __name__ == "__main__":
    check_S3_grants()
