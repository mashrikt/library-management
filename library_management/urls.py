"""library_management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path

from library_management.library.urls import author_urlpatterns, book_urlpatterns, borrow_urlpatterns

api_v1_urlpatterns = [
    path('auth/', include(('library_management.users.urls', 'users'), namespace='users')),
    path('authors/', include((author_urlpatterns, 'author'), namespace='authors')),
    path('books/', include((book_urlpatterns, 'book'), namespace='books')),
    path('borrow/', include((borrow_urlpatterns, 'borrow'), namespace='borrow')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include((api_v1_urlpatterns, 'v1'), namespace='v1')),
]
app_name = 'users'

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
