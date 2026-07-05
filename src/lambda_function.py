from src.report import generate_report
from src.notification import send_email


def lambda_handler(event, context):
    report = generate_report()

    send_email(report)

    return {
        "statusCode": 200,
        "body": "AWS Cost Optimization Report Sent Successfully"
    }