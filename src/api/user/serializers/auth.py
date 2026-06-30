from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)
    name = serializers.CharField(write_only=True, required=False, allow_blank=True)
    phone = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'phone', 'password', 'password2']
        read_only_fields = ['id']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password2': 'Passwords do not match.'})
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'email': 'Email already registered.'})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        name = validated_data.pop('name', '')
        phone = validated_data.pop('phone', '')

        first_name = ''
        last_name = ''
        if name:
            parts = [part.strip() for part in name.split(' ', 1)]
            first_name = parts[0]
            if len(parts) > 1:
                last_name = parts[1]

        user = User(**validated_data, first_name=first_name, last_name=last_name)
        if phone:
            user.phone_number = phone
        user.set_password(password)
        user.is_active = True
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid email or password.')
        if not user.is_active:
            raise serializers.ValidationError('This account is inactive.')
        data['user'] = user
        return data
