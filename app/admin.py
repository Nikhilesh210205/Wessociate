from django.contrib import admin
from .models import Idea,Token,Idea_viewed,UserProfile,Idea_bought,deal_status,bugs_and_messages,Extra_token_request,Agent_call_request

# Register your models here.

admin.site.register(Idea)
admin.site.register(Token)
admin.site.register(Idea_viewed)
admin.site.register(UserProfile)
admin.site.register(Idea_bought)
admin.site.register(deal_status)
admin.site.register(bugs_and_messages)
admin.site.register(Extra_token_request)
admin.site.register(Agent_call_request)