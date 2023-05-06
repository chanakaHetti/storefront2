from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.db.models.aggregates import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse
from . import models
from tags.models import TaggedItem

class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory' # title of the filter
    parameter_name = 'inventory' # quey string parameter on the url

    def lookups(self, request, model_admin): # What items should appear filter list
        return [
            ('<10', 'Low')
        ]
    
    def queryset(self, request, queryset): # This is the filtering logic
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)
        

class TagInline(GenericTabularInline):
    autocomplete_fields = ['tag']
    model = TaggedItem


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [TagInline]
    autocomplete_fields = ['collection']
    prepopulated_fields = {
        'slug': ['title']
    }
    actions = ['clear_inventory']
    list_display = ['title', 'unit_price', 'inventory_status']
    list_editable = ['unit_price']
    list_filter = ['collection', 'last_update', InventoryFilter]
    list_per_page = 10
    search_fields = ['title']

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'LOW'
        return 'OK'
    
    @admin.action(description='Clear Inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(invetory=0)
        self.message_user(
            request,
            f'{updated_count} products were successfuly updated'
        )


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership']
    list_editable = ['membership']
    list_per_page = 10
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'product_count']
    search_fields = ['title']

    @admin.display(ordering='product_count')
    def product_count(self, collection):
        # reverse('admin:app_model_page')
        url = (
            reverse('admin:store_product_changelist')
            + '?'
            + urlencode({
                'collection__id': str(collection.id)
            }))
        return format_html('<a href="{}">{}</a>', url, collection.product_count)
         
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            product_count=Count('product')
        )

class OrderItemInlie(admin.TabularInline):
    autocomplete_fields = ['product']
    min_num = 1
    max_num = 10
    model = models.OrderItem
    extra = 0

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    inlines = [OrderItemInlie]
    list_display = ['id', 'placed_at', 'customer']
