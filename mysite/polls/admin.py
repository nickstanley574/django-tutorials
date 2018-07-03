from django.contrib import admin

from .models import Choice, Question

# This tells Django: “Choice objects are edited on the 
# Question admin page. By default, provide enough fields 
# for 3 choices.”
#  For that reason, Django offers a tabular way of displaying inline related objects;
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3 

class QuestionAdmin(admin.ModelAdmin):
    #fields = ['pub_date','question_text']

    list_filter = ['pub_date']

    list_display = ('question_text', 'pub_date', 'was_published_recently')

    fieldsets = [
            (None,               {'fields':['question_text']}),
            ('Date information', {'fields':['pub_date']}),
    ]
    inlines = [ChoiceInline]

admin.site.register(Question, QuestionAdmin)
