from django.urls import path
from . import views


app_name = 'assignments'


urlpatterns = [
    path('list/', views.AssignmentListView.as_view(), name='list'),
    path('<int:pk>/', views.AssignmentDetailView.as_view(), name='detail'),
    path('create/', views.AssignmentCreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.AssignmentUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.AssignmentDeleteView.as_view(), name='delete'),
]