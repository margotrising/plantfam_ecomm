from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^login_process$', views.login_process),
    url(r'^logout$', views.destroy),
    url(r'^register_process$', views.register_process),
    url(r'^register_confirm$', views.register_confirm),
    url(r'^products$', views.products),
    url(r'^products/(?P<prod_id>\d+)', views.view_product),
    url(r'^add_cart/(?P<prod_id>\d+)', views.add_cart),
    url(r'^cart$', views.cart),
    url(r'^view_account/(?P<user_id>\d+)$', views.view_account),
    url(r'^admin/inventory$', views.inventory, name='inventory'),
    url(r'^admin/edit_product/(?P<prod_id>\d+)$', views.edit_product),
    url(r'^admin/edit_product_process/(?P<prod_id>\d+)$', views.edit_product_process),
    url(r'^admin/delete_product/(?P<prod_id>\d+)$', views.delete_product),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

