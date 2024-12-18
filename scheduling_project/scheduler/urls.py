from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('fcfs_sjf/', views.fcfs_sjf_page, name='fcfs_sjf_page'),
    path('dm_rm_edf_llf/', views.dm_rm_edf_llf_page, name='dm_rm_edf_llf_page'),
    path('update_process/', views.update_process, name='update_process'),
    path('delete_process/', views.delete_process, name='delete_process'),
    path('update_process_dm_rm_edf_llf/', views.update_process_dm_rm_edf_llf, name='update_process_dm_rm_edf_llf'),
]
