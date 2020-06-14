from django.contrib.auth import get_user_model, authenticate, user_logged_in
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as CoreValidationError
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from app.pkg.account.services import AuthService
from app.pkg.account.utils import get_user_token

User = get_user_model()


# ****************************************************************************
# COMMON SERIALIZERS
# ****************************************************************************

class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
    password_confirm = serializers.CharField(write_only=True)

    default_error_messages = {
        'invalid_confirm': _('Passwords don\'t match.')
    }

    def validate(self, attrs):
        attrs = super(PasswordSerializer, self).validate(attrs)
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm')

        if password != password_confirm:
            self.fail('invalid_confirm')

        try:
            validate_password(password)
        except CoreValidationError as e:
            raise serializers.ValidationError({
                'password': e.messages
            })

        return super(PasswordSerializer, self).validate(attrs)


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('auth_token',)

    auth_token = serializers.CharField(source='key')


# ****************************************************************************
# LOGIN SERIALIZER
# ****************************************************************************

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    default_error_messages = {
        'invalid_credentials': _('Invalid credentials.'),
        'does_not_exist': _('User account with this email does not exist.'),
    }

    def __init__(self, *args, **kwargs):
        super(LoginSerializer, self).__init__(*args, **kwargs)
        self.user = None

    def validate_email(self, email):
        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            self.fail('does_not_exist')

        if not user.is_active:
            self.fail('inactive_account')

        return email.lower()

    def validate(self, attrs):
        email = attrs.get('email')

        self.user = authenticate(
            email=email,
            password=attrs.get('password')
        )
        if not self.user:
            self.fail('invalid_credentials')

        return attrs

    def create(self, validated_data):
        user_logged_in.send(
            sender=self.user.__class__,
            request=self.context.get('request'), user=self.user)
        return self.user

    def to_representation(self, instance):
        return TokenSerializer(
            instance=get_user_token(self.user), context=self.context
        ).data

# ****************************************************************************
# CHANGE PASSWORD SERIALIZER
# ****************************************************************************


class ChangePasswordSerializer(PasswordSerializer):
    old_password = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    default_error_messages = {
        'wrong_password': _('Wrong old password.'),
    }

    def __init__(self, *args, **kwargs):
        super(ChangePasswordSerializer, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self, attrs):
        self.user = authenticate(email=self.instance.email, password=attrs.get('old_password'))
        if self.user is None:
            self.fail('wrong_password')

        return super(ChangePasswordSerializer, self).validate(attrs)

    def update(self, instance, validated_data):
        password = validated_data.get('password')
        AuthService.update_password(instance, password)
        return instance

    def to_representation(self, instance):
        return TokenSerializer(
            instance=get_user_token(self.user), context=self.context
        ).data

