from django.contrib import admin
from models import Occurrence, Biology, Locality
from olwidget.admin import GeoModelAdmin


# Register your models here.
class LocalityAdmin(GeoModelAdmin):
    list_display = ('locality_number', 'locality_field_number', 'name', 'date_discovered',
                    'point_x', 'point_y')
    readonly_fields = ('locality_number', 'point_x', 'point_y', 'easting', 'northing', 'date_last_modified')
    list_filter = ['date_discovered', 'formation', 'NALMA', 'region', 'county']
    search_fields = ('locality_number', 'locality_field_number', 'name')
    options = {
        'layers': ['google.terrain']
    }

class BiologyAdmin(admin.ModelAdmin):
    list_display = ('specimen_number', 'item_scientific_name', 'item_description', 'locality',
                    'date_collected', 'on_loan')
    list_filter = ['date_collected', 'on_loan', 'NALMA']

    list_per_page = 1000

admin.site.register(Occurrence)
admin.site.register(Biology, BiologyAdmin)
admin.site.register(Locality, LocalityAdmin)