from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from decimal import Decimal, InvalidOperation
from .models import Category, Product, Suppliers, Order_details, Orders
from .forms import CategoryForm, ProductForm, SuppliersForm, Order_detailsForm, OrdersForm


# BOSH SAHIFA
def index(request):
    try:
        categories = Category.objects.all()[:5]  # Faqat 5 tasi
        products = Product.objects.all().order_by('-created_at')[:8]  # Yangilari
        suppliers_count = Suppliers.objects.count()
        orders_count = Orders.objects.count()
        categories_count = Category.objects.count()
        products_count = Product.objects.count()

        return render(request, 'index.html', {
            'cat': categories,
            'pro': products,
            'suppliers_count': suppliers_count,
            'orders_count': orders_count,
            'categories_count': categories_count,
            'products_count': products_count,
        })
    except Exception as e:
        return render(request, 'index.html', {
            'cat': [], 'pro': [],
            'suppliers_count': 0, 'orders_count': 0,
            'categories_count': 0, 'products_count': 0
        })


# CATEGORY SAHIFASI
def category(request, pk):
    try:
        category_obj = get_object_or_404(Category, pk=pk)
        products = Product.objects.filter(category=category_obj)
        categories = Category.objects.all()

        return render(request, 'category.html', {
            "pro": products,
            "category": categories,
            "current_category": category_obj
        })
    except:
        return render(request, 'category.html', {
            "pro": [], "category": [], "current_category": None
        })


# ADD FUNKSIYALARI
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = Category.objects.create(
                category_name=form.cleaned_data['category_name'],
                description=form.cleaned_data['description']
            )
            messages.success(request, f'✅ "{category.category_name}" kategoriyasi qo\'shildi!')
            return redirect('home')
        else:
            messages.error(request, '❌ Formani to\'g\'ri to\'ldiring!')
    else:
        form = CategoryForm()

    return render(request, 'add_category.html', {'form': form})


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = Product.objects.create(
                product_name=form.cleaned_data['product_name'],
                unit_price=form.cleaned_data['unit_price'],
                category=form.cleaned_data['category'],
                suppliers=form.cleaned_data['suppliers'],
                photo=form.cleaned_data['photo']
            )
            messages.success(request, f'✅ "{product.product_name}" mahsuloti qo\'shildi!')
            return redirect('home')
        else:
            messages.error(request, '❌ Formani to\'g\'ri to\'ldiring!')
    else:
        form = ProductForm()

    return render(request, "add_product.html", {"form": form})


def add_suppliers(request):
    if request.method == 'POST':
        form = SuppliersForm(request.POST)
        if form.is_valid():
            supplier = Suppliers.objects.create(
                company_name=form.cleaned_data['company_name'],
                contact_name=form.cleaned_data['contact_name'],
                contact_title=form.cleaned_data['contact_title'],
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                region=form.cleaned_data['region'],
                country=form.cleaned_data['country'],
                phone=form.cleaned_data['phone']
            )
            messages.success(request, f'✅ "{supplier.company_name}" yetkazib beruvchi qo\'shildi!')
            return redirect('home')
        else:
            messages.error(request, '❌ Formani to\'g\'ri to\'ldiring!')
    else:
        form = SuppliersForm()

    return render(request, "add_suppliers.html", {"form": form})


def add_order_details(request):
    if request.method == 'POST':
        form = Order_detailsForm(request.POST)
        if form.is_valid():
            order_detail = Order_details.objects.create(
                product=form.cleaned_data['product'],
                unit_price=form.cleaned_data['unit_price'],
                quantity=form.cleaned_data['quantity']
            )
            messages.success(request, f'✅ "{order_detail.product.product_name}" buyurtma tafsiloti qo\'shildi!')
            return redirect('home')
        else:
            messages.error(request, '❌ Formani to\'g\'ri to\'ldiring!')
    else:
        form = Order_detailsForm()

    return render(request, "add_order_details.html", {"form": form})


def add_orders(request):
    if request.method == 'POST':
        form = OrdersForm(request.POST)
        if form.is_valid():
            order = Orders.objects.create(
                order_date=form.cleaned_data['order_date'],
                required_date=form.cleaned_data['required_date'],
                order_dtls=form.cleaned_data['order_dtls']
            )
            messages.success(request, f'✅ Buyurtma #{order.id} qo\'shildi!')
            return redirect('home')
        else:
            messages.error(request, '❌ Formani to\'g\'ri to\'ldiring!')
    else:
        form = OrdersForm()

    return render(request, "add_orders.html", {"form": form})


# DELETE FUNKSIYALARI
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category_name = category.category_name
        category.delete()
        messages.success(request, f'🗑️ "{category_name}" kategoriyasi o\'chirildi!')
        return redirect('home')

    return render(request, 'delete_confirm.html', {
        'object': category,
        'object_type': 'kategoriya',
        'delete_url': 'delete_category'
    })


def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product_name = product.product_name
        product.delete()
        messages.success(request, f'🗑️ "{product_name}" mahsuloti o\'chirildi!')
        return redirect('home')

    return render(request, 'delete_confirm.html', {
        'object': product,
        'object_type': 'mahsulot',
        'delete_url': 'delete_product'
    })


def delete_supplier(request, pk):
    supplier = get_object_or_404(Suppliers, pk=pk)
    if request.method == 'POST':
        supplier_name = supplier.company_name
        supplier.delete()
        messages.success(request, f'🗑️ "{supplier_name}" yetkazib beruvchi o\'chirildi!')
        return redirect('home')

    return render(request, 'delete_confirm.html', {
        'object': supplier,
        'object_type': 'yetkazib beruvchi',
        'delete_url': 'delete_supplier'
    })


def delete_order_detail(request, pk):
    order_detail = get_object_or_404(Order_details, pk=pk)
    if request.method == 'POST':
        order_detail.delete()
        messages.success(request, '🗑️ Buyurtma tafsiloti o\'chirildi!')
        return redirect('home')

    return render(request, 'delete_confirm.html', {
        'object': order_detail,
        'object_type': 'buyurtma tafsiloti',
        'delete_url': 'delete_order_detail'
    })


def delete_order(request, pk):
    order = get_object_or_404(Orders, pk=pk)
    if request.method == 'POST':
        order.delete()
        messages.success(request, '🗑️ Buyurtma o\'chirildi!')
        return redirect('home')

    return render(request, 'delete_confirm.html', {
        'object': order,
        'object_type': 'buyurtma',
        'delete_url': 'delete_order'
    })


# UPDATE FUNKSIYALARI
def update_category(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category.category_name = form.cleaned_data['category_name']
            category.description = form.cleaned_data['description']
            category.save()
            messages.success(request, f'✏️ "{category.category_name}" kategoriyasi yangilandi!')
            return redirect('home')
    else:
        form = CategoryForm(initial={
            'category_name': category.category_name,
            'description': category.description
        })

    return render(request, 'update_category.html', {
        'form': form, 'category': category
    })


def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product.product_name = form.cleaned_data['product_name']
            product.unit_price = form.cleaned_data['unit_price']
            product.category = form.cleaned_data['category']
            product.suppliers = form.cleaned_data['suppliers']

            if form.cleaned_data['photo']:
                product.photo = form.cleaned_data['photo']

            product.save()
            messages.success(request, f'✏️ "{product.product_name}" mahsuloti yangilandi!')
            return redirect('home')
    else:
        form = ProductForm(initial={
            'product_name': product.product_name,
            'unit_price': product.unit_price,
            'category': product.category,
            'suppliers': product.suppliers,
        })

    return render(request, 'update_product.html', {
        'form': form, 'product': product
    })


def update_supplier(request, pk):
    supplier = get_object_or_404(Suppliers, pk=pk)

    if request.method == 'POST':
        form = SuppliersForm(request.POST)
        if form.is_valid():
            supplier.company_name = form.cleaned_data['company_name']
            supplier.contact_name = form.cleaned_data['contact_name']
            supplier.contact_title = form.cleaned_data['contact_title']
            supplier.address = form.cleaned_data['address']
            supplier.city = form.cleaned_data['city']
            supplier.region = form.cleaned_data['region']
            supplier.country = form.cleaned_data['country']
            supplier.phone = form.cleaned_data['phone']
            supplier.save()
            messages.success(request, f'✏️ "{supplier.company_name}" yetkazib beruvchi yangilandi!')
            return redirect('home')
    else:
        form = SuppliersForm(initial={
            'company_name': supplier.company_name,
            'contact_name': supplier.contact_name,
            'contact_title': supplier.contact_title,
            'address': supplier.address,
            'city': supplier.city,
            'region': supplier.region,
            'country': supplier.country,
            'phone': supplier.phone,
        })

    return render(request, 'update_supplier.html', {
        'form': form, 'supplier': supplier
    })


def update_order_detail(request, pk):
    order_detail = get_object_or_404(Order_details, pk=pk)

    if request.method == 'POST':
        form = Order_detailsForm(request.POST)
        if form.is_valid():
            order_detail.product = form.cleaned_data['product']
            order_detail.unit_price = form.cleaned_data['unit_price']
            order_detail.quantity = form.cleaned_data['quantity']
            order_detail.save()
            messages.success(request, '✏️ Buyurtma tafsiloti yangilandi!')
            return redirect('home')
    else:
        form = Order_detailsForm(initial={
            'product': order_detail.product,
            'unit_price': order_detail.unit_price,
            'quantity': order_detail.quantity,
        })

    return render(request, 'update_order_detail.html', {
        'form': form, 'order_detail': order_detail
    })


def update_order(request, pk):
    order = get_object_or_404(Orders, pk=pk)

    if request.method == 'POST':
        form = OrdersForm(request.POST)
        if form.is_valid():
            order.order_date = form.cleaned_data['order_date']
            order.required_date = form.cleaned_data['required_date']
            order.order_dtls = form.cleaned_data['order_dtls']
            order.save()
            messages.success(request, f'✏️ Buyurtma #{order.id} yangilandi!')
            return redirect('home')
    else:
        form = OrdersForm(initial={
            'order_date': order.order_date,
            'required_date': order.required_date,
            'order_dtls': order.order_dtls,
        })

    return render(request, 'update_order.html', {
        'form': form, 'order': order
    })