from django.urls import path

from .views import (
    TrainerCreate,
    TrainerDetail,
    TrainerEdit,
    TrainerList
)


urlpatterns = [
    path('create', TrainerCreate.as_view(), name='trainer-create'),
    path('list', TrainerList.as_view(), name='trainer-list'),
    path('<str:name>/edit', TrainerEdit.as_view(), name='trainer-edit'),
    path('<str:name>', TrainerDetail.as_view(), name='trainer'),
]
