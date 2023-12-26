from Accounts.models import MessageModel, AccountModel
from django.core.management.base import BaseCommand


messages = [
    {
        "header": "Warm Welcome and Introduction to Our Platform",
        "message": "We extend a warm welcome to you as you join our platform! We're truly excited to have you here and look forward to providing you with an exceptional experience. If you ever have any questions or require assistance, please don't hesitate to reach out to our dedicated support team."
    },
    {
        "header": "Important Company Announcement: Latest Updates and Improvements",
        "message": "We are thrilled to share some significant news with our valued users. Our team has been hard at work, and we are excited to introduce the latest updates and improvements to our platform. For a detailed overview of these changes, please visit our website or app. We believe these enhancements will elevate your experience with us to new heights."
    },
    {
        "header": "Stay Informed with Our Informative Newsletter",
        "message": "Stay informed and up-to-date with our informative newsletter! By subscribing, you'll receive the latest news, expert tips, and valuable updates directly in your inbox. It's a fantastic way to ensure you're always in the know about what's happening in our community and industry."
    },
    {
        "header": "Expressing Our Sincere Gratitude for Your Feedback",
        "message": "We wanted to take a moment to express our heartfelt gratitude for taking the time to provide us with your invaluable feedback. Your insights are incredibly important to us, and they play a pivotal role in helping us continually improve and enhance our services. Thank you for being an integral part of our journey."
    },
    {
        "header": "Save the Date: Upcoming Event You Won't Want to Miss",
        "message": "We're excited to announce a special upcoming event that is sure to be a highlight on your calendar. Mark [Event Date] on your schedule and prepare to join us for a day filled with excitement, entertainment, and memorable experiences. Stay tuned for more details, and get ready to make unforgettable memories with us!"
    }
]


class MessageData:
    def generate_instances(self):
        account_instances = AccountModel.objects.all()
        for account_instance in account_instances:
            for message in messages:
                MessageModel.objects.create(
                    account_relation=account_instance,
                    header=message["header"],
                    message=message["message"],
                    is_active=True
                )


class Command(BaseCommand):
    def generate(self):
        try:
            MessageData().generate_instances()
        except Exception as e:
            print(e)
            pass

    def handle(self, *args, **kwargs):
        self.generate()
