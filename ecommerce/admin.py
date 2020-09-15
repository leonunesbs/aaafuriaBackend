from django.contrib import admin
from .models import Item, ItemSize, OrderItem, Order, Payment


class OrderItemAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'item',
        'size',
        'quantity',
        'ordered',
    ]
    list_filter = [
        'item',
        'ordered',
    ]
    search_fields = [
        'user__username',
        'user__sócio__nome_completo',
    ]
    actions = [
        'export_as_csv',
    ]

    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(
            meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field)
                                   for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"


admin.site.register(Item)
admin.site.register(ItemSize)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Order)
admin.site.register(Payment)
