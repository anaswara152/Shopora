from django.urls import path
from user import views

urlpatterns=[
    path('',views.home,name='home'),
    path('registration',views.registration,name='registration'),
    path('login_user',views.login_user,name='login_user'),
    path('logoutuser',views.logoutuser,name='logoutuser'),
    path('userhome',views.userhome,name='userhome'),
    path('deatiles/<int:id>',views.deatiles,name='deatiles'),
    path('addcart',views.addcart,name='addcart'),
    path('viewcart',views.viewcart,name='viewcart'),
    path('trash/<int:id>',views.trash,name='trash'),
    path('addproduct/<int:id>',views.addproduct,name='addproduct'),
    path('deletecart/<int:id>',views.deletecart,name='deletecart'),
    path('addwhis/<int:id>',views.addwhis,name='addwhis'),
    path('toggle_wishlist/<int:id>',views.toggle_wishlist,name='toggle_wishlist'),
    path('viewwish',views.viewwish,name='viewwish'),
    path('payment_page',views.payment_page,name='payment_page'),
    path('place_order',views.place_order,name='place_order'),
    path('process_payment',views.process_payment,name='process_payment'),
    path('save_order',views.save_order,name='save_order'),
    path('complete_online_payment',views.complete_online_payment,name='complete_online_payment'),
    path('my_orders',views.my_orders,name='my_orders'),
    path('my_order_details/<int:order_id>',views.my_order_details,name='my_order_details'),
    path('user_cancel_order/<int:order_id>',views.user_cancel_order,name='user_cancel_order'),
    path('deletecart/<int:id>',views.deletecart,name='deletecart'),
    path('view_profile',views.view_profile,name='view_profile'),
    path('edit_profile',views.edit_profile,name='edit_profile'),
    path('forgot_password',views.forgot_password,name='forgot_password'),
    path('remove-wishlist/<int:wish_id>/', views.removewish, name='removewish'),
    path('payment-success/<int:order_id>/', views.payment_success, name='payment_success'),
    path('cod-success/<int:order_id>/', views.cod_success, name='cod_success'),



]
