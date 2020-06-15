from rest_framework import serializers

from app.pkg.domains.choices import Status
from app.pkg.domains.models import BlockedDomain, BlockRequest
from app.pkg.domains.utils import get_ip_from_request


# ****************************************************************************
# DOMAIN SERIALIZER
# ****************************************************************************

class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlockedDomain
        fields = '__all__'


# ****************************************************************************
# DOMAIN BLOCK REQUEST SERIALIZER
# ****************************************************************************

class DomainBlockRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlockRequest
        fields = ('domain', 'user_email', 'description',)

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data.update({
            'user_ip': get_ip_from_request(request)
        })

        instance = BlockRequest.objects.create(**validated_data)
        return instance


# ****************************************************************************
# DOMAIN STATUS SERIALIZERS
# ****************************************************************************

class BaseReviewSerializer(serializers.Serializer):
    new_status = NotImplemented

    def update(self, instance, validated_data):
        instance.status = self.new_status
        instance.save()
        return instance


class ApproveBlockSerializer(BaseReviewSerializer):
    new_status = Status.APPROVED.value

    def update(self, instance, validated_data):
        instance = super(ApproveBlockSerializer, self).update(instance, validated_data)
        BlockedDomain.objects.update_or_create({'domain': instance.domain})
        return instance


class RefuseBlockSerializer(BaseReviewSerializer):
    new_status = Status.REFUSED.value
