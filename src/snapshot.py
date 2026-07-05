import boto3
from datetime import datetime, timezone

ec2 = boto3.client("ec2")


def get_all_snapshots():
    """
    Returns all snapshots owned by your AWS account.
    """
    response = ec2.describe_snapshots(OwnerIds=["self"])

    snapshots = []

    for snapshot in response["Snapshots"]:
        snapshots.append({
            "SnapshotId": snapshot["SnapshotId"],
            "VolumeId": snapshot["VolumeId"],
            "StartTime": snapshot["StartTime"],
            "State": snapshot["State"],
            "VolumeSize": snapshot["VolumeSize"]
        })

    return snapshots


def get_old_snapshots(days=30):
    """
    Returns snapshots older than the specified number of days.
    """
    now = datetime.now(timezone.utc)

    old_snapshots = []

    for snapshot in get_all_snapshots():
        age = (now - snapshot["StartTime"]).days

        if age > days:
            snapshot["AgeInDays"] = age
            old_snapshots.append(snapshot)

    return old_snapshots