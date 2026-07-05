from src.ec2 import get_stopped_instances
from src.ebs import get_unattached_volumes
from src.snapshot import get_old_snapshots
from src.eip import get_unused_elastic_ips
from src.s3 import get_all_buckets
from src.rds import get_all_rds_instances


def generate_report():
    report = []

    report.append("=" * 70)
    report.append("        AWS COST OPTIMIZATION REPORT")
    report.append("=" * 70)

    # EC2
    report.append("\nStopped EC2 Instances")
    report.append("-" * 70)

    stopped = get_stopped_instances()

    if stopped:
        for instance in stopped:
            report.append(
                f"{instance['InstanceId']} | {instance['InstanceType']} | {instance['AvailabilityZone']}"
            )
    else:
        report.append("No stopped EC2 instances.")

    # EBS
    report.append("\nUnused EBS Volumes")
    report.append("-" * 70)

    volumes = get_unattached_volumes()

    if volumes:
        for volume in volumes:
            report.append(
                f"{volume['VolumeId']} | {volume['Size']} GB | {volume['VolumeType']}"
            )
    else:
        report.append("No unattached EBS volumes.")

    # Snapshots
    report.append("\nOld Snapshots")
    report.append("-" * 70)

    snapshots = get_old_snapshots()

    if snapshots:
        for snapshot in snapshots:
            report.append(
                f"{snapshot['SnapshotId']} | {snapshot['AgeInDays']} days"
            )
    else:
        report.append("No old snapshots.")

    # Elastic IP
    report.append("\nUnused Elastic IPs")
    report.append("-" * 70)

    eips = get_unused_elastic_ips()

    if eips:
        for ip in eips:
            report.append(ip["PublicIp"])
    else:
        report.append("No unused Elastic IPs.")

    # S3
    report.append("\nS3 Buckets")
    report.append("-" * 70)

    buckets = get_all_buckets()

    if buckets:
        for bucket in buckets:
            report.append(bucket["BucketName"])
    else:
        report.append("No S3 buckets.")

    # RDS
    report.append("\nRDS Instances")
    report.append("-" * 70)

    databases = get_all_rds_instances()

    if databases:
        for db in databases:
            report.append(
                f"{db['DBInstanceIdentifier']} | {db['Engine']} | {db['Status']}"
            )
    else:
        report.append("No RDS instances.")

    return "\n".join(report)