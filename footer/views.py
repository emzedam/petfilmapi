from rest_framework import viewsets
from .models import FooterDescription, FooterLink
from .serializers import FooterDescriptionSerializer, FooterLinkSerializer

# ViewSet برای توضیحات درباره سایت، فقط خواندنی
class FooterDescriptionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FooterDescription.objects.all()
    serializer_class = FooterDescriptionSerializer

# ViewSet برای لینک‌های فوتر، فقط خواندنی
class FooterLinkViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FooterLink.objects.all()
    serializer_class = FooterLinkSerializer
