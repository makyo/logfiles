from django.urls import (
    include,
    path,
)

from log import api


api = [
    path('logs/', api.list_logs),
    path('log/<int:log_id>/', api.get_log),
]

patterns = [
    path('api/v1/', include(api)),
]
