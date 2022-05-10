import json
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from .dashboard import category_data, brand_data, order_data
# Create your views here.


@staff_member_required
def dashboard(request):
    # Render Product segmentation

    category_chart_data = category_data()
    # brands segmentation
    brand_chart_data = brand_data()
    order_chart_data = order_data()

    context = {
        'category_wise_pie_data': json.dumps(category_chart_data),
        'brand_data': json.dumps(brand_chart_data),
        'order_data': json.dumps(order_chart_data)
    }

    return render(request, 'dashboard/admin_dashboard.html', context)
