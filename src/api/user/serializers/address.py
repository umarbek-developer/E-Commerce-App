from rest_framework import serializers

from apps.users.models import Address


class AddressSerializer(serializers.ModelSerializer):
    zip = serializers.CharField(source='zip_code', required=False, allow_blank=False)

    class Meta:
        model = Address
        fields = ['id', 'street', 'city', 'state', 'zip', 'country', 'is_default', 'label']
        read_only_fields = ['id']
