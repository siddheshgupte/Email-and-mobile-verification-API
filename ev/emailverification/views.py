from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.mail import send_mail
import random, string
from django.core.signing import Signer
from . serializers import EmailVerificationSerializer
from . models import Email
from django.utils import timezone


# To send mail fill the EMAIL_HOST_USER and EMAIL_HOST_PASSWORD in settings.py

# We will use the inbuilt encryption which will the encrypt a value as value:encryption
signer = Signer()


@api_view(['POST'])
def EmailVerification(request):
    # If a user asks for verification mail, we first check if that user already exists in the database
    try:
        user = Email.objects.get(email_id=request.data["email_id"])
        # If user exists and is unverified this means he
        # already has a verification code which we have to replace
        # (Logged off without verifying, Lost the verification email, didn't receive the verification email)
        if user.is_verified==False:
            # Generate a new verification code
            user.verification_code = ''.join(random.choice(string.lowercase) for i in range(10))
            user.save()
            # New verification link
            content = {"message": "New Verification Email sent too your Mail ID",
                       "new_link": 'http://127.0.0.1:8000/email_verification_link/' + signer.sign(
                        request.data["email_id"]) + "/" + request.data["verification_code"],
                     }
            message = 'Verification link is http://127.0.0.1:8000/email_verification_link/' + signer.sign(
                request.data["email_id"]) + '/' + request.data["verification_code"]
            send_mail('Hi', message, 'abc@gmail.com', (request.data["email_id"],), fail_silently=True)
            return Response(content, content_type='application/json')
        # If user exists and is verified already
        else:
            return Response({"message": "Already verified"}, content_type='application/json')
    except Email.DoesNotExist:
        serializer = EmailVerificationSerializer(data=request.data)
        # Generate a random verification code and store it in the database
        serializer.initial_data["verification_code"] = ''.join(random.choice(string.lowercase) for i in range(10))
        # Sanity check for email
        if serializer.is_valid():
            serializer.save()
            # Link included in the response for clarity
            content={"message": "Verification Email sent too your Mail ID",
                     "link": 'http://127.0.0.1:8000/email_verification_link/'+signer.sign(serializer.data["email_id"])+"/"+serializer.data["verification_code"],
                     }
            # Create the validation Link
            message='Verification link is http://127.0.0.1:8000/email_verification_link/'+signer.sign(serializer.data["email_id"])+'/'+serializer.data["verification_code"]
            # To send mail fill the EMAIL_HOST_USER and EMAIL_HOST_PASSWORD in settings.py
            # Replace 'abc@gmail.com' with your email id as a string or settings.EMAIL_HOST_USER
            send_mail('Hi', message, 'abc@gmail.com', (serializer.data["email_id"],), fail_silently=True)
            return Response(content, status=status.HTTP_201_CREATED, content_type='application/json')
        else:
            # Error message if wrong email format
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# User will come here after clicking the validation link
@api_view(['GET'])
def EmailVerificationLink(request, encrypted_email_id, verification_code):
    # Decrypt the encrypted email_id
    eid = signer.unsign(encrypted_email_id)
    try:
        # Check if in the database
        user = Email.objects.get(email_id=eid)
    except Email.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if user.verification_code == verification_code:
        # If verification code matches update is_verified and updated_at
        user.is_verified = True
        user.updated_at = timezone.now()
        user.save()
        content = {"message": "Email Verified",
                }
    else:
        content={
            "message": "Email not verified,Retry"
            }
        # Return the corresponding message
    return Response(content,content_type='application/json')
