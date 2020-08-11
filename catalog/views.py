from django.shortcuts import render
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import csv
import datetime
from django.http import HttpResponse

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

from catalog.forms import RenewBookForm
from catalog.models import Book,Author,BookInstance,Genre

# Create your views here.
@login_required
def index(request):

	#tracking number of vists to our local lib home page using sessions
	num_vist = request.session.get('num_vist',0)
	request.session['num_vist'] = num_vist + 1

	#general count for some of the main objects to be displayed at the home page

	num_of_books = Book.objects.all().count()
	num_of_book_copies = BookInstance.objects.all().count()
	#available books(status available)
	num_of_book_copies_available = BookInstance.objects.filter(status__exact='a').count()
	#num of authors
	num_of_authors = Author.objects.count() #all() is implied by default
	context = {
		'num_of_books' : num_of_books,
		'num_of_book_copies' : num_of_book_copies,
		'num_of_book_copies_available' : num_of_book_copies_available,
		'num_of_authors' : num_of_authors,
		'num_vist' : num_vist,
	}

#render our html to display the context

	return render(request,'catalog/index.html',context=context)

#using class based generic view

class BookListView(generic.ListView):
	model = Book
	pignate_by = 10

	#specifying context name to override default one
	context_object_name = 'book_list'

class BookDetailView(generic.DetailView):

	model = Book

class AuthorListView(generic.ListView):
	model = Author

class AuthorDetailView(generic.DetailView):
	model = Author

class BookCopyListView(generic.ListView):
	model = BookInstance


def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)
    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        book_renewal_form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if book_renewal_form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = book_renewal_form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        book_renewal_form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': book_renewal_form,
        'book_instance': book_instance,
        }

    return render(request, 'catalog/book_renew_librarian.html', context)
class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
	"""Generic class-based view listing books on loan to current user."""
	models = BookInstance
	template_name = 'catalog/bookinstance_list_borrowed_user.html'
	paginate_by = 10

	def get_queryset(self):
		return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

#exporting csv file for printing 
def export_books_csv(request):
	response = HttpResponse(content_type = 'text/csv')
	response['Content-Disposition'] = 'attachment; filename="books.csv"'

	write = csv.writer(response)
	write.writerow(['title', 'author', 'isbn'])
	books = Book.objects.all().values_list('title', 'author', 'isbn')

	for book in books:
		write.writerow(book)
	return response