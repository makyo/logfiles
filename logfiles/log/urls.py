from django.urls import (
    include,
    path,
)

from log import (
    api,
    views,
)


api = [
    path('logs/', api.list_logs),
    path('log/<int:log_id>/', api.get_log),
    path('log/<int:log_id>/join-lines/', api.join_lines),
    path('line/<int:line_id>/set/', api.set_line_type),
    path('line/<int:line_id>/tag/add/', api.add_line_tag),
    path('line/<int:line_id>/tag/remove/', api.remove_line_tag),
]

patterns = [
    path('', views.app),
    path('api/v1/', include(api)),
]
