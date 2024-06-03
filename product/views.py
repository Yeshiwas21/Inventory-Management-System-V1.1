from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Request
from django.contrib import messages
from django.utils.decorators import method_decorator
from .forms import  ProductForm, CategoryForm, RequestProductForm
from django.views import View
from django.views.generic import View
from django.utils import timezone
from django.urls import reverse


# Create your views here.


@login_required
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.added_by = request.user
            product.save()
            messages.success(request, 'Product created successfully!')
            return redirect('product_list')
    else:
        form = ProductForm()

    return render(request, 'products/create_product.html', {'form': form})

@login_required
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You Have added a new product successfully.')
            return redirect('create_product')
    else:
        form = CategoryForm()

    return render(request, 'products/create_category.html', {'form': form})


@login_required(login_url='login')
def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})


@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    
    # Filter requests based on storekeeper_approval_status
    approved_requests = Request.objects.filter(product=product, storekeeper_approval_status='approved').order_by('id')
    pending_requests = Request.objects.filter(product=product, storekeeper_approval_status='pending').order_by('id')
    rejected_requests = Request.objects.filter(product=product, storekeeper_approval_status='rejected').order_by('id')

    return render(request, 'products/product_detail.html', {'product': product, 'approved_requests': approved_requests, 'pending_requests': pending_requests, 'rejected_requests': rejected_requests})


@login_required
def product_detail_for_admin(request, product_id):
    product = Product.objects.get(pk=product_id)
    approved_requests = Request.objects.filter(product=product, admin_approval_status='approved').order_by('id')
    pending_requests = Request.objects.filter(product=product, admin_approval_status='pending').order_by('id')
    rejected_requests = Request.objects.filter(product=product, admin_approval_status='rejected').order_by('id')


    return render(request, 'products/product_detail_for_admin.html', {'product': product, 'approved_requests': approved_requests, 'pending_requests': pending_requests, 'rejected_requests': rejected_requests})

@login_required
def request_product(request, product_id):
    product = Product.objects.get(pk=product_id)

    if request.method == 'POST':
        request_form = RequestProductForm(request.POST)
        if request_form.is_valid():
            quantity = request_form.cleaned_data['quantity']
            additional_info = request_form.cleaned_data['additional_info']

            ### Creating Product Instances
            request_instance = Request.objects.create(
                product=product,
                requested_by=request.user,
                quantity=quantity,
                storekeeper_approved_by=None,
                admin_approved_by=None,
                storekeeper_approved_date=None,
                admin_approved_date=None,
                additional_info=additional_info
            )
            requested_quantity = request_instance.quantity
            messages.success(request, f'Request for  {product.name} sent successfully.')

            return redirect('product_list')
            
    else:
        request_form = RequestProductForm()

    return render(request, 'products/request_product.html', {'request_form': request_form, 'product': product})


class StoreKeeperView(View):
    template_name = 'products/storekeeper.html'

    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        pending_requests = Request.objects.filter(storekeeper_approval_status='pending')

        return render(request, self.template_name, {'products': products, 'pending_requests': pending_requests})
    

@method_decorator(login_required, name='dispatch')
class AdminView(View):
    template_name = 'products/adminview.html'

    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        pending_requests = Request.objects.filter(admin_approval_status='pending')

        return render(request, self.template_name, {'products': products, 'pending_requests': pending_requests})

@method_decorator(login_required, name='dispatch')
class StoreKeeperApprovalView(View):
    template_name = 'inventory/store_keeper_approval.html'

    def get(self, request, product_id, *args, **kwargs):
        product = get_object_or_404(Product, id=product_id)
        requests = Request.objects.filter(product=product, storekeeper_approval_status='pending').order_by('id')

        # Provide a new instance of the form for GET requests
        form = RequestProductForm()

        return render(request, self.template_name, {'product': product, 'requests': requests, 'form': form})

    def post(self, request, product_id, *args, **kwargs):
        product = get_object_or_404(Product, id=product_id)
        requests = Request.objects.filter(product=product, storekeeper_approval_status='pending').order_by('id')

        form = RequestProductForm(request.POST)

        if form.is_valid():
            request_instance_id = form.cleaned_data.get('request_id')
            if request_instance_id:
                request_instance = Request.objects.get(pk=request_instance_id)

                requested_quantity = form.cleaned_data['quantity']

                if request_instance.admin_approval_status == 'rejected':
                    request_instance.storekeeper_approval_status = 'pending'
                    messages.error(request, 'Admin is already Rejected this request.')
                                    


                if requested_quantity <= product.quantity:
                    # Update product assignment
                    product.storekeeper_approval_status = 'approved'
                    product.save()

                    # Update request status to 'approved'
                    request_instance.storekeeper_approval_status = 'approved'
                    request_instance.storekeeper_approved_by = request.user
                    request_instance.storekeeper_approved_date = timezone.now()
                    request_instance.save()

                    # Display a success message
                    messages.success(request, f'Request for {requested_quantity} {product.name} approved by storekeeper.')

                    # You can add additional logic for notifications or redirects

                    return redirect('product_detail', product_id=product.id)
                else:
                    # Handle case where requested quantity exceeds available quantity
                    form.add_error('quantity', 'Requested quantity exceeds available quantity.')
            else:
                # Handle case where 'request_id' is missing
                form.add_error(None, 'Invalid request. Please try again.')

        # If form is not valid, re-render the template with errors
        return render(request, self.template_name, {'product': product, 'requests': requests, 'form': form})
    
@method_decorator(login_required, name='dispatch')
class StoreKeeperRejectView(View):

    def get(self, request, product_id, *args, **kwargs):
        product = get_object_or_404(Product, id=product_id)
        requests = Request.objects.filter(product=product, storekeeper_approval_status='pending').order_by('id')

        return render(request, self.template_name, {'product': product, 'requests': requests})

    def post(self, request, product_id, *args, **kwargs):
        product = get_object_or_404(Product, id=product_id)
        requests = Request.objects.filter(product=product, storekeeper_approval_status='pending').order_by('id')

        # Update status to 'rejected'
        for request_instance in requests:
            if request_instance.storekeeper_approval_status == 'pending':
                request_instance.storekeeper_approval_status = 'rejected'
                request_instance.save()

        # Display a success message
        messages.success(request, f'Requests for {product.name} rejected by storekeeper.')

        # You can add additional logic for notifications or redirects

        return redirect('store_keeper')  # Replace with the actual URL name for the store keeper view



@method_decorator(login_required, name='dispatch')
class AdminApprovalView(View):
    template_name = 'products/admin_approval.html'

    def get(self, request, product_id, *args, **kwargs):
        product = get_object_or_404(Product, id=product_id)
        requests = Request.objects.filter(product=product, admin_approval_status='pending').order_by('id')

        # Provide a new instance of the form for GET requests
        form = RequestProductForm()

        return render(request, self.template_name, {'product': product, 'requests': requests, 'form': form})

    def post(self, request, product_id, *args, **kwargs):
        product = get_object_or_404(Product, id=product_id)
        requests = Request.objects.filter(product=product, admin_approval_status='pending').order_by('id')

        form = RequestProductForm(request.POST)

        if form.is_valid():
            request_instance_id = form.cleaned_data.get('request_id')
            if request_instance_id:
                request_instance = Request.objects.get(pk=request_instance_id)

                # Check if the storekeeper has approved the request
                if request_instance.storekeeper_approval_status == 'pending':
                    messages.error(request, 'Storekeeper approval is required before admin approval.')
                    return render(request, self.template_name, {'product': product, 'requests': requests, 'form': form})
                if request_instance.storekeeper_approval_status == 'rejected':
                    messages.error(request, 'You Can not approve, Storekeeper Rejected it.')
                    return render(request, self.template_name, {'product': product, 'requests': requests})

                requested_quantity = form.cleaned_data['quantity']

                if requested_quantity <= product.quantity:
                    # Decrease the product quantity
                    product.quantity -= requested_quantity
                    product.save()

                    # Update product assignment
                    product.admin_approval_status = 'approved'
                    product.save()

                    # Update request status to 'approved'
                    request_instance.admin_approval_status = 'approved'
                    request_instance.assignet_to = request_instance.requested_by
                    request_instance.admin_approved_by = request.user
                    request_instance.admin_approved_date = timezone.now()
                    request_instance.save()

                    # Display a success message
                    messages.success(request, f'Request for {requested_quantity} {product.name} approved by admin.')

                    # You can add additional logic for notifications or redirects

                    return redirect('product_detail', product_id=product.id)
                else:
                    # Handle case where requested quantity exceeds available quantity
                    form.add_error('quantity', 'Requested quantity exceeds available quantity.')
            else:
                # Handle case where 'request_id' is missing
                form.add_error(None, 'Invalid request. Please try again.')

        # If form is not valid, re-render the template with errors
        return render(request, self.template_name, {'product': product, 'requests': requests, 'form': form})


@method_decorator(login_required, name='dispatch')
class AdminRejectView(View):

    def get(self, request, product_id, *args, **kwargs):
        product = get_object_or_404(Product, id=product_id)
        requests = Request.objects.filter(product=product, storekeeper_approval_status='pending').order_by('id')

        return render(request, self.template_name, {'product': product, 'requests': requests})

    def post(self, request, product_id, *args, **kwargs):
        product = get_object_or_404(Product, id=product_id)
        requests = Request.objects.filter(product=product, admin_approval_status='pending').order_by('id')

        # Update status to 'rejected'
        for request_instance in requests:
            if request_instance.admin_approval_status == 'pending':
                request_instance.admin_approval_status = 'rejected'
                request_instance.save()

        # Display a success message
        messages.success(request, f'Requests for {product.name} rejected by Admin.')

        # You can add additional logic for notifications or redirects

        return redirect('admin_view')  # Replace with the actual URL name for the store keeper view


def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        edit_form = ProductForm(request.POST, instance=product)

        if edit_form.is_valid():
            product = edit_form.save(commit=False)
            # Additional logic if needed
            product.save()
            messages.success(request, f'{product.name} updated successfully.')
            return redirect('product_list')
    else:
        edit_form = ProductForm(instance=product)

    return render(request, 'products/edit_product.html', {'edit_form': edit_form, 'product': product})


class DeleteProductView(View):
    def post(self, request, product_id, *args, **kwargs):
        product = get_object_or_404(Product, id=product_id)
        product.delete()
        messages.success(request, f'{product.name} has been deleted successfully.')
        return redirect('product_list')

    def get(self, request, product_id, *args, **kwargs):
        product = get_object_or_404(Product, id=product_id)
        return render(request, 'products/delete_product.html', {'product': product})


@login_required
def user_products(request):
    # Retrieve the user's assigned requests where assignet_to is not null
    assigned_requests = Request.objects.filter(assignet_to=request.user, assignet_to__isnull=False)

    return render(request, 'products/user_products.html', {'assigned_requests': assigned_requests})

def user_requests_status(request):
    user = request.user

    # Retrieve all requests for the user
    user_requests = Request.objects.filter(requested_by=user)

    return render(request, 'products/request_status.html', {'user_requests': user_requests})