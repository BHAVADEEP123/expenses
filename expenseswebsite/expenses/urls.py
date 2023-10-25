from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('',views.index, name='expenses'),
    path('add-expense',views.add_expense,name='add-expenses'),
    path('edit-expense/<int:id>',views.expense_edit,name='edit-expenses'),
    path('delete-expense/<int:id>',views.expense_delete,name='delete-expense'),
    path('search-data',csrf_exempt(views.search_data),name='search-data'),
    path('expense_category_summary', views.expense_category_summary,name="expense_category_summary"),
    path('stats', views.stats_view,name="expense-stats"),
    path('export-csv',views.export_csv,"export-csv"),
]