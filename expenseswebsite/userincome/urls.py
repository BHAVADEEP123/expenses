from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('',views.index, name='income'),
    path('add-income',views.add_income,name='add-income'),
    path('edit-income/<int:id>',views.income_edit,name='edit-income'),
    path('delete-income/<int:id>',views.income_delete,name='delete-income'),
    path('search-data2',csrf_exempt(views.search_data),name='search-data2'),
    path('income_category_summary', views.income_category_summary,name="income_category_summary"),
    path('stats', views.stats_view,name="income-stats")
]