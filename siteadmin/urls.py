from django.urls import path
from siteadmin import views

urlpatterns=[
    path('adminhome',views.adminhome,name='adminhome'),
    path('productadd',views.productadd,name='productadd'),
    path('viewproduct',views.viewproduct,name='viewproduct'),
    path('productedit/<int:id>',views. productedit,name='productedit'),
    path('deleteproduct/<int:id>',views.deleteproduct,name='deleteproduct'),
    path('adminview',views.adminview,name='adminview'),
    path('detailsshow/<int:id>',views.detailsshow,name='detailsshow'),
    path('processing_orders',views.processing_orders,name='processing_orders'),
    path('complete_order/<int:id>',views.complete_order,name='complete_order'),
    path('cancel_processing/<int:id>',views.cancel_processing,name='cancel_processing'),
    path('admin_orders',views.admin_orders,name='admin_orders')
]
