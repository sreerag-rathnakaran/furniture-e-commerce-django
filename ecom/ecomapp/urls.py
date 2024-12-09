from django.urls import path
from . import views

urlpatterns =[
    path('',views.index, name='index'),
    path('cart/',views.cart, name='cart'),
    path('sellers/',views.sellers,name='sellers'),
    path('shop/', views.shop, name='shop'),
    path('order/', views.order, name='order'),
    path('cancel_order/<int:id>', views.cancel_order, name='cancel_order'),
    path('display_orders/', views.display_orders, name='display_orders'),
    path('p_b_on_category/<str:category>/',views.p_b_on_category,name='p_b_on_category'),
    path('add_review/',views.add_review,name='add_review'),
    path('blog/',views.blog,name='blog'),


    path('Proceed_to_checkout_from_cart/', views.Proceed_to_checkout_from_cart, name='Proceed_to_checkout_from_cart'),
    path('Proceed_to_checkout/<int:id>', views.Proceed_to_checkout, name='Proceed_to_checkout'),
    path('explore/', views.explore, name='explore'),
    path('add_to_cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
    # path('update_cart_quantity/<int:id>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('increasequantity/<int:id>/', views.increasequantity, name='increasequantity'),
    path('decreasequantity/<int:id>/', views.decreasequantity, name='decreasequantity'),
    path('Proceed_to_payment/',views.Proceed_to_payment,name='Proceed_to_payment'),
    path('Proceed_to_payment2/<int:id>',views.Proceed_to_payment2,name='Proceed_to_payment2'),
    path('create-payment/<int:id>/', views.onlinepayment, name='create-payment'),
    path('verify-payment/', views.verify_razor_payment, name='verify-payment'),
    path('cod/<int:id>', views.cod, name='cod'),

    path('adminpage/',views.admin,name='adminpage'),
    path('display_customer/',views.display_customer,name='display_customer'),
    path('display_seller/',views.display_seller,name='display_seller'),
    path('approve_seller/<int:id>',views.approve_seller,name='approve_seller'),
    path('approved_seller/',views.approved_seller,name='approved_seller'),
    path('approve_or_cancel_seller/',views.approve_or_cancel_seller,name='approve_or_cancel_seller'),
    path('reject_seller/<int:id>',views.reject_seller,name='reject_seller'),
    path('display_products_basedonseller/<int:id>',views.display_products_basedonseller,name='display_products_basedonseller'),

    path('register_seller/', views.register_seller, name='register_seller'),
    path('Login_admin_or_seller',views.Login_admin_or_seller,name='Login_admin_or_seller'),
    path('display_sellerforadmin/',views.display_sellerforadmin,name='display_sellerforadmin'),
    path('update_seller/<int:id>',views.update_seller,name='update_seller'),
    path('update_sellerdetails/<int:id>',views.update_sellerdetails,name='update_sellerdetails'),
    path('Logout/',views.Logout,name='Logout'),
    
    path('addcategory/',views.addcategory,name='addcategory'),
    path('add_category/',views.add_category,name='add_category'),
    path('display_category/',views.display_category,name='display_category'),
    path('update_category/<int:id>',views.update_category ,name='update_category'),
    path('update_categorydetails/<int:id>',views.update_categorydetails ,name='update_categorydetails'),
    path('delete_category/<int:id>',views.delete_category ,name='delete_category'),

    path('addproduct/',views.addproduct,name='addproduct'),
    path('add_product/',views.add_product,name='add_product'),
    path('display_product/',views.display_product,name='display_product'),
    path('update_product/<int:id>',views.update_product ,name='update_product'),
    path('update_productdetails/<int:id>',views.update_productdetails ,name='update_productdetails'),
    path('delete_product/<int:id>',views.delete_product ,name='delete_product'),
    path('single_productpage/<int:id>',views.single_productpage ,name='single_productpage'),
    
    path('Payment/',views.Payment ,name='Payment'),
    path('Payment2/',views.Payment2 ,name='Payment2'),
    path('search/',views.search, name='search'),
    path('offerproducts',views.offerproducts,name='offerproducts'),


    path('register_customer/', views.register_customer, name='register_customer'),
    path('LoginCustomer/',views.LoginCustomer,name='LoginCustomer'),
    path('LogoutCustomer',views.LogoutCustomer,name='LogoutCustomer'),
    path('userprofile/',views.userprofile,name='userprofile'),
    path('update_customer/<int:id>',views.update_customer,name='update_customer'),
    path('update_customerdetails/<int:id>',views.update_customerdetails,name='update_customerdetails'),

    path('orderstatus/',views.orderstatus,name='orderstatus'),
    path('shipped/<int:id>',views.shipped,name='shipped'),
    path('delivered/<int:id>',views.delivered,name='delivered'),
    path('shipped_orders/',views.shipped_orders,name='shipped_orders'),
    path('delivered_orders/',views.delivered_orders,name='delivered_orders'),



    # path('', views.product_list, name='product_list'),
    # path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    # path('category/<int:category_id>/', views.category_list, name='category_list'),
    # path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    # path('cart/', views.cart_detail, name='cart_detail'),
    # path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    # path('order/create/', views.create_order, name='create_order'),
    # path('order/<int:order_id>/', views.order_detail, name='order_detail')

]