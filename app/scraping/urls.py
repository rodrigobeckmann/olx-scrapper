from django.urls import path
from .views import product_selection, scraped_data_list, archive_selected

urlpatterns = [
    path('', product_selection, name='product_selection'),
    path('scraped-data/<int:product_id>/', scraped_data_list, name='scraped_data_list'),
    path('archive-selected/', archive_selected, name='archive_selected'),
]