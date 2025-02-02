from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL
    path('about/', view=views.get_about, name="about"),
    path('contact/', view=views.get_contact, name="contact"),

    # path for registration
    path('signup/', views.registration_request, name='signup'),

    # path for login
    path('login/', views.login_request, name='login'),

    # path for logout
    path('logout/', views.logout_request, name='logout'),

    path('', views.get_dealerships, name='index'),

    # path for dealer reviews view
    path('dealer/<int:dealer_id>/', views.get_dealer_details, name='dealer_details'),

    # path for add a review view
    path('addreview/<int:dealer_id>/', views.add_review, name='add_review')


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
