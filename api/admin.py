from django.contrib import admin

import api.models


admin.site.register(api.models.BlackList)
admin.site.register(api.models.Client)
admin.site.register(api.models.Payment)
admin.site.register(api.models.Page)
admin.site.register(api.models.Transport)