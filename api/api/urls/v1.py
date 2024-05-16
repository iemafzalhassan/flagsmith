from app_analytics.views import SDKAnalyticsFlags, SelfHostedTelemetryAPIView
from django.conf import settings
from django.conf.urls import url
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import authentication, permissions, routers

from environments.identities.traits.views import SDKTraits
from environments.identities.views import SDKIdentities
from environments.sdk.views import SDKEnvironmentAPIView
from features.views import SDKFeatureStates
from integrations.github.views import github_webhook
from organisations.views import chargebee_webhook

schema_view = get_schema_view(
    openapi.Info(
        title="Flagsmith API",
        default_version="v1",
        description="",
        license=openapi.License(name="BSD License"),
        contact=openapi.Contact(email="support@flagsmith.com"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    authentication_classes=[authentication.SessionAuthentication],
)

traits_router = routers.DefaultRouter()
traits_router.register(r"", SDKTraits, basename="sdk-traits")

app_name = "v1"

urlpatterns = [
    url(r"^organisations/", include("organisations.urls"), name="organisations"),
    url(r"^projects/", include("projects.urls"), name="projects"),
    url(r"^environments/", include("environments.urls"), name="environments"),
    url(r"^features/", include("features.urls"), name="features"),
    url(r"^multivariate/", include("features.multivariate.urls"), name="multivariate"),
    url(r"^segments/", include("segments.urls"), name="segments"),
    url(r"^users/", include("users.urls")),
    url(r"^e2etests/", include("e2etests.urls")),
    url(r"^audit/", include("audit.urls")),
    url(r"^auth/", include("custom_auth.urls")),
    url(r"^metadata/", include("metadata.urls")),
    # Chargebee webhooks
    url(r"cb-webhook/", chargebee_webhook, name="chargebee-webhook"),
    # GitHub integration webhook
    url(r"github-webhook/", github_webhook, name="github-webhook"),
    # Client SDK urls
    url(r"^flags/$", SDKFeatureStates.as_view(), name="flags"),
    url(r"^identities/$", SDKIdentities.as_view(), name="sdk-identities"),
    url(r"^traits/", include(traits_router.urls), name="traits"),
    url(r"^analytics/flags/$", SDKAnalyticsFlags.as_view(), name="analytics-flags"),
    url(
        r"^analytics/telemetry/$",
        SelfHostedTelemetryAPIView.as_view(),
        name="analytics-telemetry",
    ),
    url(
        r"^environment-document/$",
        SDKEnvironmentAPIView.as_view(),
        name="environment-document",
    ),
    url("", include("features.versioning.urls", namespace="versioning")),
    # API documentation
    url(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    url(
        r"^docs/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]

if settings.SPLIT_TESTING_INSTALLED:
    from split_testing.views import (
        ConversionEventTypeView,
        CreateConversionEventView,
        SplitTestViewSet,
    )

    split_testing_router = routers.DefaultRouter()
    split_testing_router.register(r"", SplitTestViewSet, basename="split-tests")

    urlpatterns += [
        url(
            r"^split-testing/", include(split_testing_router.urls), name="split-testing"
        ),
        url(
            r"^split-testing/conversion-events/",
            CreateConversionEventView.as_view(),
            name="conversion-events",
        ),
        path(
            "conversion-event-types/",
            ConversionEventTypeView.as_view(),
            name="conversion-event-types",
        ),
    ]
