from django.shortcuts import render
from .models import WebManual, MobileManual, AdminPanelManual
from django.views import View

class WebManualView(View):
    web = WebManual.objects.all()
    def get(self, request):
        return render(request,'web_manual.html', {'webs': self.web})


class MobileManualView(View):
    mobile = MobileManual.objects.all()
    def get(self, request):
        return render(request, 'mobile_manual.html', {'mobiles': self.mobile})

class AdminManualView(View):
    admin = AdminPanelManual.objects.all()
    def get(self, request):
        return render(request, 'admin_manual.html', {'admins': self.admin})