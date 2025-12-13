from django.shortcuts import render
from accounts.decorators import admin_required


@admin_required
def admin_dashboard(request):
    return render(request, "dashboard/admin_dashboard.html")
