from django.contrib import admin
from .models import Member

# mamgeorge, q_1_Z_DJ
# Register your models here.

class MemberAdmin(admin.ModelAdmin):
	list_display = ("firstname", "lastname", "joined_date",)

admin.site.register(Member, MemberAdmin)