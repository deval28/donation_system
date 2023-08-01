from rest_framework.routers import DefaultRouter

from . import views

app_name = "donation_system"
router = DefaultRouter()

router.register("user", views.UserViewSet, basename="user")
router.register("charity", views.CharityViewSet, basename="donation_system")
router.register("donation", views.DonationViewSet, basename="donation")


urlpatterns = []

urlpatterns += router.urls
