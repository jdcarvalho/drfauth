from django.contrib import admin
from app_api.models import Country


class CountryModelAdmin(admin.ModelAdmin):
    search_fields = ('name', 'acronym')
    fields = ['acronym', 'name',]
    ordering = ('name',)

    class Meta:
        model = Country


admin.site.register(Country, CountryModelAdmin)

