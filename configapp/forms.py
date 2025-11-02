from django import forms
from django.core.exceptions import ValidationError
from datetime import datetime
from .models import Category, Suppliers, Product, Order_details

class CategoryForm(forms.Form):
    category_name = forms.CharField(
        max_length=100,
        label='Kategoriya Nomi',
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Kategoriya nomini kiriting..."
        })
    )
    description = forms.CharField(
        label='Tavsif',
        required=False,
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 4,
            "placeholder": "Kategoriya tavsifini kiriting..."
        })
    )

    def clean_category_name(self):
        category_name = self.cleaned_data['category_name']
        if not category_name[0].isupper():
            raise ValidationError("Kategoriya nomi bosh harf bilan boshlanishi kerak!")
        if any(char.isdigit() for char in category_name):
            raise ValidationError("Kategoriya nomida raqam bo'lmasligi kerak!")
        return category_name

class ProductForm(forms.Form):
    product_name = forms.CharField(
        max_length=100,
        label='Mahsulot Nomi',
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Mahsulot nomini kiriting..."
        })
    )
    unit_price = forms.DecimalField(
        label='Narxi',
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "0.00",
            "step": "0.01"
        })
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label='Kategoriya',
        widget=forms.Select(attrs={"class": "form-control"})
    )
    suppliers = forms.ModelChoiceField(
        queryset=Suppliers.objects.all(),
        label='Yetkazib Beruvchi',
        widget=forms.Select(attrs={"class": "form-control"})
    )
    photo = forms.ImageField(
        label='Mahsulot Rasmi',
        required=False,
        widget=forms.FileInput(attrs={"class": "form-control"})
    )

    def clean_product_name(self):
        product_name = self.cleaned_data['product_name']
        invalid_chars = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '=', '{', '}', '[', ']', '|', '\\', ':', ';', '"', "'", '<', '>', ',', '.', '?', '/']
        if any(char in product_name for char in invalid_chars):
            raise ValidationError("Mahsulot nomida maxsus belgilar bo'lmasligi kerak!")
        return product_name

    def clean_unit_price(self):
        unit_price = self.cleaned_data['unit_price']
        if unit_price <= 1:
            raise ValidationError("Narx 1$ dan baland bo'lishi kerak!")
        if unit_price > 10:
            raise ValidationError("Narx 10$ dan past bo'lishi kerak!")
        return unit_price

class SuppliersForm(forms.Form):
    company_name = forms.CharField(
        max_length=100,
        label='Kompaniya Nomi',
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Kompaniya nomini kiriting..."
        })
    )
    contact_name = forms.CharField(
        max_length=100,
        label='Aloqa Shaxsi',
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Aloqa shaxsini kiriting..."
        })
    )
    contact_title = forms.CharField(
        max_length=100,
        label='Lavozim',
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Lavozimini kiriting..."
        })
    )
    address = forms.CharField(
        label='Manzil',
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 3,
            "placeholder": "To'liq manzilni kiriting..."
        })
    )
    city = forms.CharField(
        max_length=100,
        label='Shahar',
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Shaharni kiriting..."
        })
    )
    region = forms.CharField(
        max_length=100,
        label='Viloyat',
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Viloyatni kiriting..."
        })
    )
    country = forms.CharField(
        max_length=100,
        label='Mamlakat',
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Mamlakatni kiriting..."
        })
    )
    phone = forms.CharField(
        max_length=20,
        label='Telefon',
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "+998901234567"
        })
    )

    def clean_city(self):
        city = self.cleaned_data['city']
        if not city[0].isupper():
            raise ValidationError("Shahar nomi bosh harf bilan boshlanishi kerak!")
        return city

    def clean_region(self):
        region = self.cleaned_data['region']
        if not region[0].isupper():
            raise ValidationError("Viloyat nomi bosh harf bilan boshlanishi kerak!")
        return region

    def clean_country(self):
        country = self.cleaned_data['country']
        if not country[0].isupper():
            raise ValidationError("Mamlakat nomi bosh harf bilan boshlanishi kerak!")
        return country

class Order_detailsForm(forms.Form):
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        label='Mahsulot',
        widget=forms.Select(attrs={"class": "form-control"})
    )
    unit_price = forms.DecimalField(
        label='Birlik Narxi',
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "0.00",
            "step": "0.01"
        })
    )
    quantity = forms.IntegerField(
        label='Miqdor',
        min_value=1,
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "1"
        })
    )

class OrdersForm(forms.Form):
    order_date = forms.DateTimeField(
        label='Buyurtma Sanasi',
        widget=forms.DateTimeInput(attrs={
            "class": "form-control",
            "type": "datetime-local"
        })
    )
    required_date = forms.DateTimeField(
        label='Talab Qilingan Sana',
        widget=forms.DateTimeInput(attrs={
            "class": "form-control",
            "type": "datetime-local"
        })
    )
    order_dtls = forms.ModelChoiceField(
        queryset=Order_details.objects.all(),
        label='Buyurtma Tafsiloti',
        widget=forms.Select(attrs={"class": "form-control"})
    )

    def clean_order_date(self):
        order_date = self.cleaned_data['order_date']
        min_date = datetime(2025, 1, 1)
        if order_date < min_date:
            raise ValidationError("Buyurtma sanasi 2025-01-01 dan keyin bo'lishi kerak!")
        return order_date