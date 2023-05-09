from django.contrib import admin
from .models import WebManual, MobileManual,AdminPanelManual

admin.site.register(WebManual)
admin.site.register(MobileManual)
admin.site.register(AdminPanelManual)