from django.urls import path
from .import views

urlpatterns = [

	path('',views.index,name='index'),
	path('books/',views.BookListView.as_view(),name='books'),
	path('book/<int:pk>',views.BookDetailView.as_view(),name='book-detail'),
	path('authors',views.AuthorListView.as_view(),name='authors'),
	path('author/<int:pk>',views.AuthorDetailView.as_view(),name='author-detail'),
	path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
	path('book-copies/',views.BookCopyListView.as_view(),name='copies'),
	#csv export url
	path('export/csv',views.export_books_csv, name='export_books_csv'),
	path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
]
