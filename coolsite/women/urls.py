from django.urls import path, re_path
from women.views import *
from django.views.decorators.cache import cache_page
urlpatterns = [
    # path('', index, name='home'),
    # path('', cache_page(60)(WomenHome.as_view()), name='home'), кэширование на уровне view
    path('', WomenHome.as_view(), name='home'),
    path('about/', about, name='about'),
    # path('addpage/', add_page, name='add_page'),
    path('addpage/', AddPage.as_view(), name='add_page'),
    path('contact/', Contact.as_view(), name='contact'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', WomenCategory.as_view(), name='category'),
    # path('category/<int:cat_id>/', show_category, name='category'),
    # path('cats/<int:catid>/', categories),
    # re_path(r'^archive/(?P<year>[0-9]{4})/', archive)
]
