import imp
from django.db.models import Count, Sum, Q
from django.db.models.functions import TruncMonth
from Store.models import Products, Order, OrderItem


def category_data():

    products = Products.objects.values(
        'category__title').annotate(total=Count('id'))

    category_data_source = {
        'name': "Categories Data",
        "data": []
    }

    for key in products:
        data = {
            'name': key['category__title'],
            'y': key['total'],
        }
        category_data_source['data'].append(data)

    category_chart_data = {
        'chart': {'type': 'pie'},
        'title': {'text': "Product Segmentation"},
        'setOptions': {
            'lang': {
                'thousandsSep': ','
            }
        },
        'accessibility': {
            'announceNewData': {
                'enabled': True
            }
        },
        'plotOptions': {
            'series': {
                'dataLabels': {
                    'enabled': True,
                    'format': '{point.name}: <br>{point.percentage:.1f} %<br>total: {point.y}',
                    'padding': 0,
                    'style': {
                        'fontSize': '10px'
                    }
                }
            }
        },
        'tooltip': {
            'headerFormat': '<span style="font-size:11px; color:#8e5ea2">{series.name}<br>{point.percentage:.1f} %'
            '</span><br>',
            'pointFormat': '<span style="color:#3cba9f">{point.name}</span>: <b>{point.y}</b><br/>'

        },
        'series': [category_data_source],
    }

    return category_chart_data


def brand_data():
    segment = Products.objects.values('brand').annotate(
        totalCount=Count('id')).order_by('-totalCount')[:10]

    brand_data_source = {
        'name': "Brand Names",
        "data": []
    }

    for coys in segment:
        data = {
            'name': coys['brand'],
            'y': coys['totalCount'],
        }

        brand_data_source['data'].append(data)

    brand_chart_data = {
        'chart': {'type': 'column'},
        'title': {'text': "Top 10 Brands"},
        'setOptions': {
            'lang': {
                'thousandsSep': ','
            }
        },
        'accessibility': {
            'announceNewData': {
                'enabled': True
            }
        },
        'plotOptions': {
            'series': {
                'dataLabels': {
                    'enabled': True,
                    'format': '{point.name}: <br>total: {point.y}',
                    'padding': 0,
                    'style': {
                        'fontSize': '10px'
                    }
                }
            }
        },
        'tooltip': {
            'headerFormat': '<span style="font-size:11px; color:#8e5ea2">{series.name}<br>{point.percentage:.1f} %'
            '</span><br>',
            'pointFormat': '<span style="color:#3cba9f">{point.name}</span>: <b>{point.y}</b><br/>'

        },
        'series': [brand_data_source],
    }
    return brand_chart_data


def order_data():
    orders = Order.objects.values('payment_status').annotate(
        count=Count('id'))

    order_data_source = {
        'name': "Orders Made",
        "data": []
    }

    for status in orders:
        data = {
            'name': status['payment_status'],
            'y': status['count'],
        }
        if data['name'] == "C":
            data["name"] = "Completed Orders"
            data["color"] = 'green'
        elif data["name"] == "P":
            data["name"] = "Pending Orders"
            data["color"] = 'yellow'
        else:
            data["name"] = "Failed Orders"
            data["color"] = 'red'

        order_data_source['data'].append(data)

    order_chart_data = {
        'chart': {'type': 'bar', 'backgroundColor': 'whitesmoke'},
        'title': {'text': "Order Analysis"},
        'setOptions': {
            'lang': {
                'thousandsSep': ','
            }
        },

        'accessibility': {
            'announceNewData': {
                'enabled': True
            }
        },
        'plotOptions': {
            'series': {
                'dataLabels': {
                    'enabled': True,
                    'format': '{point.name}: <br>total: {point.y}',
                    'padding': 0,
                    'style': {
                        'fontSize': '10px'
                    }
                }
            }
        },
        'tooltip': {
            'headerFormat': '<span style="font-size:11px; color:#8e5ea2">{series.name}<br>{point.percentage:.1f} %'
            '</span><br>',
            'pointFormat': '<span style="color:#3cba9f">{point.name}</span>: <b>{point.y}</b><br/>'

        },
        'series': [order_data_source],
    }
    return order_chart_data


# def order_revenue():
#     orders = Order.objects.filter(payment_status="C").values(
#         'order_placed_at').annotate(sum=Sum('orderitem.getrevenue'))

#     print(orders)
