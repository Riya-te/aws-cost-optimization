import boto3

ec2 = boto3.client("ec2")


def get_all_elastic_ips():
    """
    Returns all Elastic IP addresses.
    """
    response = ec2.describe_addresses()

    elastic_ips = []

    for address in response["Addresses"]:
        elastic_ips.append({
            "PublicIp": address.get("PublicIp"),
            "AllocationId": address.get("AllocationId"),
            "AssociationId": address.get("AssociationId"),
            "InstanceId": address.get("InstanceId"),
        })

    return elastic_ips


def get_unused_elastic_ips():
    """
    Returns Elastic IPs that are not associated with any instance.
    """
    unused_ips = []

    for ip in get_all_elastic_ips():
        if ip["AssociationId"] is None:
            unused_ips.append(ip)

    return unused_ips