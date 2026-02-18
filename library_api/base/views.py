from django.shortcuts import render
from .forms import BookForm
from .models import Book
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Book
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes   # 👈 add this
from rest_framework.permissions import AllowAny



# Create your views here.

def home(request):
    books = Book.objects.all()
    return render(request, 'base/home.html', { 'books': books })

def search(request):
    return render(request, 'base/search.html')

def addBook(request):
    form = BookForm()
    return render(request, 'base/book.html', { 'form': form, 'script_filepath': '/static/js/add_book.js', 'method_type': 'POST' })

def updateBook(request, pk):
    book = Book.objects.get(id=pk)
    form = BookForm(instance=book)
    return render(request, 'base/book.html', { 'form': form, 'script_filepath': '/static/js/update_book.js', 'method_type': 'PATCH' })



@csrf_exempt
def add_book(request):
    if request.method == "GET":
        form = BookForm()
        return render(request, 'base/book.html', {
            'form': form,
            'script_filepath': '/static/js/add_book.js',
            'method_type': 'POST'
        })

    if request.method == "POST":
        try:
            data = json.loads(request.body.decode('utf-8'))

            book = Book.objects.create(
                title=data.get('title'),
                author=data.get('author'),
                genre=data.get('genre'),
                publishing_year=int(data.get('publishing_year')) if data.get('publishing_year') else None,
                pages=int(data.get('pages')) if data.get('pages') else None,
                chapters=int(data.get('chapters')) if data.get('chapters') else None,
            )

            return JsonResponse({"message": "Book added"}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_book(request, pk):
    try:
        book = Book.objects.get(id=pk)
        book.delete()
        return Response({"message": "Book deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except Book.DoesNotExist:
        return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

