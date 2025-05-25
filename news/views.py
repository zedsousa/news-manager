from django.db.models import Q
from rest_framework import permissions, viewsets

from .models import News
from .serializers import NewsSerializer


class NewsViewSet(viewsets.ModelViewSet):
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == "admin":
            return News.objects.all()

        if user.role == "editor":
            return News.objects.filter(
                Q(author=user)
                | (
                    Q(status="published")
                    & (
                        Q(is_pro=False)
                        | (
                            Q(is_pro=True)
                            & Q(vertical__in=user.plan.verticals.all())
                            & Q(author__plan__is_pro=True)
                        )
                    )
                )
            ).distinct()

        if user.role == "reader":
            return News.objects.filter(
                Q(status="published")
                & (
                    Q(is_pro=False)
                    | (
                        Q(is_pro=True)
                        & Q(vertical__in=user.plan.verticals.all())
                        & Q(author__plan__is_pro=True)
                    )
                )
            ).distinct()

        return News.objects.none()
