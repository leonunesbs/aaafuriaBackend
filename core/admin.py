from django.contrib import admin
from .models import Sócio, Financeiro, Associação, AssociaçãoCategoria


admin.site.register(Sócio)
admin.site.register(Financeiro)
admin.site.register(Associação)
admin.site.register(AssociaçãoCategoria)
