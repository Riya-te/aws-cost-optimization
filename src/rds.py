import boto3

rds = boto3.client("rds")


def get_all_rds_instances():
    """
    Returns all RDS database instances.
    """
    response = rds.describe_db_instances()

    databases = []

    for db in response["DBInstances"]:
        databases.append({
            "DBInstanceIdentifier": db["DBInstanceIdentifier"],
            "Engine": db["Engine"],
            "DBInstanceClass": db["DBInstanceClass"],
            "Status": db["DBInstanceStatus"],
            "AllocatedStorage": db["AllocatedStorage"],
            "MultiAZ": db["MultiAZ"],
            "Endpoint": db.get("Endpoint", {}).get("Address", "N/A")
        })

    return databases


def get_available_rds_instances():
    """
    Returns RDS instances that are in the 'available' state.
    """
    return [
        db for db in get_all_rds_instances()
        if db["Status"] == "available"
    ]