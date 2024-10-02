

import requests
from django.core.mail import send_mail

class SendOtpCode:
    def __init__(self , receiver , password):
        self.receiver = receiver
        self.password = password

    def send_by_sms(self):
        url = "https://ippanel.com/api/select"
        payload = {
            "op": "pattern",
            "user": "9142766601",
            "pass": "Mh@36463646",
            "fromNum": "+983000505",
            "toNum": self.receiver,
            "patternCode": "yk2kv2b0d1m43wk",
            "inputData": [
                {
                    "verification-code": self.password
                }
            ]
        }

        try:
            response = requests.post(url, json=payload)

            if response.status_code == 200:
                return True
            else:
                return False

        except requests.exceptions.RequestException as e:
            return False
        
    
    def send_by_email(self):
        subject = "کد احراز هویت پت فیلم"
        message = f"کد تایید شما در پت فیلم:‌ {self.password}"
        recipient_email = self.receiver

        try:
            # ارسال ایمیل
            send_mail(
                subject,
                message,
                'info@alish.co.ir',  # فرستنده
                [recipient_email],  # گیرنده‌ها
                fail_silently=False,
            )

            return True

        except Exception as e:
            return False

