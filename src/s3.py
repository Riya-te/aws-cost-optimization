import boto3

s3 = boto3.client("s3")


def get_all_buckets():
    """
    Returns all S3 buckets.
    """
    response = s3.list_buckets()

    buckets = []

    for bucket in response["Buckets"]:
        buckets.append({
            "BucketName": bucket["Name"],
            "CreationDate": bucket["CreationDate"]
        })

    return buckets


def get_bucket_count():
    """
    Returns the total number of S3 buckets.
    """
    return len(get_all_buckets())