from rest_framework import permissions, viewsets

from apps.users.models import Address

from ..serializers import AddressSerializer


class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        self._handle_default_flag(serializer)
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        self._handle_default_flag(serializer)
        serializer.save()

    def _handle_default_flag(self, serializer):
        if serializer.validated_data.get('is_default'):
            Address.objects.filter(user=self.request.user, is_default=True).update(is_default=False)
