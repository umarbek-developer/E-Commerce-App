from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .address import AddressSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True, read_only=True)
    name = serializers.CharField(required=False, allow_blank=True)
    phone = serializers.CharField(source='phone_number', required=False, allow_blank=True)
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'phone', 'role', 'is_active', 'addresses']
        read_only_fields = ['id', 'role', 'is_active']

    def get_role(self, obj):
        return 'admin' if obj.is_staff else 'customer'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['name'] = instance.get_full_name() or instance.email
        data['phone'] = instance.phone_number
        return data

    def update(self, instance, validated_data):
        name = validated_data.pop('name', None)
        phone = validated_data.pop('phone_number', None)
        if name is not None:
            parts = [part.strip() for part in name.split(' ', 1)]
            instance.first_name = parts[0]
            instance.last_name = parts[1] if len(parts) > 1 else ''
        if phone is not None:
            instance.phone_number = phone
        instance.save()
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Old password is incorrect.')
        return value

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
