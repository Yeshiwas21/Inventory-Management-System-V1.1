from django.urls import path
from .views import (
    create_product, product_list, create_category, request_product, 
    product_detail, StoreKeeperApprovalView, StoreKeeperView, StoreKeeperRejectView,
    AdminApprovalView, AdminView, product_detail_for_admin, AdminRejectView,
    edit_product, user_products,user_requests_status, DeleteProductView
)

urlpatterns = [
    path('create_product/', create_product, name='create_product'),
    path('create_category/', create_category, name='create_category'),
    path('product_list/', product_list, name='product_list'),
    path('product-detail/<int:product_id>/', product_detail, name='product_detail'),
    path('product-detail-admin/<int:product_id>/', product_detail_for_admin, name='product_detail_admin'),
    path('edit-product/<int:product_id>/', edit_product, name='edit_product'),
    path('delete-product/<int:product_id>/', DeleteProductView.as_view(), name='delete_product'),
    path('user-products/', user_products, name='user_products'),
    path('user-requests/', user_requests_status, name='user_requests_status'),
    # New URL pattern
    path('request-product/<int:product_id>/',request_product, name='request_product'),
    path('storekeeper/', StoreKeeperView.as_view(), name='store_keeper'),
    path('admin_view/', AdminView.as_view(), name='admin_view'),

    path('store-keeper-approval/<int:product_id>/', StoreKeeperApprovalView.as_view(), name='store_keeper_approval'),
    path('storekeeper-reject/<int:product_id>/', StoreKeeperRejectView.as_view(), name='store_keeper_reject'),
    path('admin-reject/<int:product_id>/', AdminRejectView.as_view(), name='admin_reject'),
    path('admin-approval/<int:product_id>/', AdminApprovalView.as_view(), name='admin_approval'),



]


