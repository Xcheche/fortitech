from django.contrib import admin

from contacts.models import Contact

# Register your models here.


class ContactAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "email",
        "phone",
        "purpose",
    )


admin.site.register(Contact, ContactAdmin)
