
from django.urls import path
from . import views

urlpatterns = [

    path('' , views.store, name='store'),
    path('<int:id>/' , views.detail_view, name='detail'),
    path('chart/' , views.cart, name='chart'),
    path('checkout/' , views.checkout, name='checkout'),
    path('update_item/' , views.updateItem, name='update_item'),
    path('process_order/' , views.processOrder, name='process_order'),

]
