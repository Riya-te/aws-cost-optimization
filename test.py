from src.report import generate_report
from src.notification import send_email

report = generate_report()

print(report)

response = send_email(report)

print(response)