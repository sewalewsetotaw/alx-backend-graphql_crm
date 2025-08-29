import django_filters
from crm.models import Customer, Product, Order

class CustomerFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    email = django_filters.CharFilter(field_name="email", lookup_expr="icontains")
    createdAtGte = django_filters.DateFilter(field_name="created_at", lookup_expr="gte")
    createdAtLte = django_filters.DateFilter(field_name="created_at", lookup_expr="lte")
    phone = django_filters.CharFilter(method="filter_phone_pattern")

    def filter_phone_pattern(self, queryset, name, value):
        return queryset.filter(phone__startswith=value)

    class Meta:
        model = Customer
        fields = ["name", "email", "createdAtGte", "createdAtLte", "phone"]

class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    priceGte = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    priceLte = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    stockGte = django_filters.NumberFilter(field_name="stock", lookup_expr="gte")
    stockLte = django_filters.NumberFilter(field_name="stock", lookup_expr="lte")
    class Meta:
        model = Product
        fields = ["name", "priceGte", "priceLte", "stockGte", "stockLte"]

class OrderFilter(django_filters.FilterSet):
    totalAmountGte = django_filters.NumberFilter(field_name="total_amount", lookup_expr="gte")
    totalAmountLte = django_filters.NumberFilter(field_name="total_amount", lookup_expr="lte")
    orderDateGte = django_filters.DateFilter(field_name="order_date", lookup_expr="gte")
    orderDateLte = django_filters.DateFilter(field_name="order_date", lookup_expr="lte")
    
    customerName = django_filters.CharFilter(field_name="customer__name", lookup_expr="icontains")
    productName = django_filters.CharFilter(field_name="products__name", lookup_expr="icontains")
    productId = django_filters.NumberFilter(field_name="products__id")
    class Meta:
        model = Order
        fields = [ "totalAmountGte",
            "totalAmountLte",
            "orderDateGte",
            "orderDateLte",
            "customerName",
            "productName",
            "productId",]

