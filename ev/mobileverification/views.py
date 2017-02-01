from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . serializers import MobileSerializer
from . models import Mobile
from django.utils import timezone
import random
from twilio.rest import TwilioRestClient
from . credentials import account_sid, auth_token, my_cell, my_twilio

# Twilio has been used for sending sms
# The corresponding credentials are in credentials.py

# Use cases are identical to email verification
@api_view(['POST'])
def SmsVerification(request):
    try:
        # Check if user exists in database
        user=Mobile.objects.get(mobile_no=request.data["mobile_no"])
        if user.is_verified==False:
            # User exists but is not verified
            # Didn't receive the message, Deleted the message, Exited the app and didn't enter OTP for a long time, Battery went off
            # Create new OTP and send and also store this in the db
            user.OTP=(''.join(str(random.randint(0,9)) for i in xrange(6)))
            user.save()
            msg = "Your OTP is:" + user.OTP
            client = TwilioRestClient(account_sid, auth_token)
            client.messages.create(to=my_cell, from_=my_twilio, body=msg)
            content = {"message": "new OTP sent to your number",
                       }
            return Response(content, status=status.HTTP_201_CREATED, content_type='application/json')
        else:
            # User exists and is already verified
            return Response({"message": "Already verified"}, status=status.HTTP_201_CREATED, content_type='application/json')

    except Mobile.DoesNotExist:
        # Similar to email verification( Generate OTP and send the sms to the user)
        serializer = MobileSerializer(data=request.data)
        serializer.initial_data["OTP"] = ''.join(str(random.randint(0,9)) for i in xrange(6))
        if serializer.is_valid():
            client=TwilioRestClient(account_sid, auth_token)
            msg="Your OTP is:"+serializer.initial_data["OTP"]
            client.messages.create(to=my_cell,from_=my_twilio, body=msg)
            serializer.save()
            content = {"message": "OTP sent to your number",
                       }
            return Response(content, status=status.HTTP_201_CREATED, content_type='application/json')
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def MobileOtpVerification(request):
    try:
        # Check if user is in the database
        user = Mobile.objects.get(mobile_no=request.data["mobile_no"])
    except Mobile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if user.OTP == request.data["OTP"]:
        user.is_verified = True
        user.updated_at = timezone.now()
        user.save()
        content = {"message": "Mobile number Verified"}
    else:
        # Wrong info
        content={"message": "Mobile number not Verified,Retry"}
    return Response(content, content_type='application/json')





