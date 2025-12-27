from django.contrib import admin

from ISLtranslatorApp.models import ComplaintTable, FeedbackTable, LoginTable, UserTable

# Register your models here.
admin.site.register(LoginTable)
admin.site.register(UserTable)
admin.site.register(ComplaintTable)
admin.site.register(FeedbackTable)