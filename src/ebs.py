import boto3

ec2 = boto3.client("ec2")


def get_all_volumes():
    """
    Returns all EBS volumes.
    """
    response = ec2.describe_volumes()

    volumes = []

    for volume in response["Volumes"]:
        volumes.append({
            "VolumeId": volume["VolumeId"],
            "Size": volume["Size"],
            "State": volume["State"],
            "VolumeType": volume["VolumeType"],
            "AvailabilityZone": volume["AvailabilityZone"]
        })

    return volumes


def get_unattached_volumes():
    """
    Returns only unattached EBS volumes.
    """
    volumes = get_all_volumes()

    return [
        volume for volume in volumes
        if volume["State"] == "available"
    ]