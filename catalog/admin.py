from django.contrib import admin
from .models import Author,Genre,Book,BookInstance

# Register your models here.
#admin.site.register(Author)
class AuthorAdmin(admin.ModelAdmin):
	list_display = ('last_name','first_name','date_of_birth','date_of_death')
	fields = ['first_name','last_name',('date_of_birth','date_of_death')]
admin.site.register(Author,AuthorAdmin)

#admin.site.register(Book)
class BookAdmin(admin.ModelAdmin):
	list_display = ('title','author','display_genre')

admin.site.register(Book,BookAdmin)

admin.site.register(Genre)
class BookInstanceAdmin(admin.ModelAdmin):
	list_display = ('book','due_back','borrower')
	list_filter = ('status','due_back')

	fieldsets = (
       (None, {
            'fields': ('book', 'imprint', 'id')
        }),
       
        ('Availability', {
            'fields': ('status', 'due_back','borrower')
        }),
    )

admin.site.register(BookInstance,BookInstanceAdmin)
#admin.site.register(BookInstance)
