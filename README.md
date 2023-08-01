# Donation System using Django and Django Rest Framework

APIs for a donation system

The repo includes a Django project with multiple functionalities like:
 - Login with OTP by integrating with Twilio
 - User, charity and donation details
 - Donation History by the charity(receiver) and donor,
 - RazorPay - Payment Gateway Integrated

There is Postman Collection attached and a management command **dummy_data** to create default users.

**# -------------------------------- Environment Variables --------------------------------------------**

SECRET_KEY="YOUR SECRET KEY"
DEBUG=True

# --------------------------------------- Twilio Credentials ------------------------------------
AUTH_TOKEN="YOUR TWILIO AUTH TOKEN"
Account_SID="YOUR TWILIO REGISTERED ACCOUNT SID"


# ------------------------------ RazorPay Credentials -------------------------------------------
key_id="YOUR RAZORPAY KEY ID"
key_secret="YOUR RAZORPAY KEY SECRET"



