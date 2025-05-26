from django.db.models import Q
from rest_framework import permissions, viewsets

from .models import News
from .permissions import IsAuthorOrAdmin
from .serializers import NewsSerializer


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrAdmin]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        user = self.request.user

        if user.role == "admin":
            return News.objects.all()

        filters = Q(status="published") & (
            Q(is_pro=False)
            | (
                Q(is_pro=True)
                & Q(vertical__in=user.plan.verticals.all())
                & Q(author__plan__is_pro=True)
            )
        )

        if user.role == "editor":
            return News.objects.filter(Q(author=user) | filters).distinct()

        if user.role == "reader":
            return News.objects.filter(filters).distinct()

        return News.objects.none()
