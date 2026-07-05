import boto3

sns = boto3.client("sns")

TOPIC_ARN = "arn:aws:sns:ap-south-1:898711548122:CostOptimizationTopic"


def send_email(report):
    """
    Sends the AWS Cost Optimization Report via SNS.
    """

    response = sns.publish(
        TopicArn=TOPIC_ARN,
        Subject="AWS Cost Optimization Report",
        Message=report
    )

    return response