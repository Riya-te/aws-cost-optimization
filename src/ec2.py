import boto3

ec2 = boto3.client("ec2")


def get_all_instances():
    """
    Returns all EC2 instances with their details.
    """
    response = ec2.describe_instances()

    instances = []

    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:

            instances.append({
                "InstanceId": instance["InstanceId"],
                "State": instance["State"]["Name"],
                "InstanceType": instance["InstanceType"],
                "AvailabilityZone": instance["Placement"]["AvailabilityZone"]
            })

    return instances


def get_stopped_instances():
    """
    Returns only stopped EC2 instances.
    """
    instances = get_all_instances()

    stopped = [
        instance for instance in instances
        if instance["State"] == "stopped"
    ]

    return stopped