from rest_framework import serializers
from . models import Email


class EmailVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = ('email_id', 'verification_code',)
