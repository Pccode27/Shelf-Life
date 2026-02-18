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



@require_POST
def add_books(request):
    """
    Expects JSON body: { "books": [ {book1}, {book2}, ... ] }
    Returns: { "added": [...], "skipped": [...] }
    """
    try:
        payload = json.loads(request.body.decode('utf-8'))
        books = payload.get('books', [])
    except Exception:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    added = []
    skipped = []

    for b in books:
        title = b.get('title')
        if not title:
            continue
        # Prevent duplicates by title; change this if you want a different dedupe rule
        if Book.objects.filter(title=title).exists():
            skipped.append({"title": title, "reason": "already_exists"})
            continue

        book = Book.objects.create(
            title=title,
            author=b.get('author', ''),
            genre=b.get('genre', ''),
            publishing_year=b.get('publishing_year') or None,
            pages=b.get('pages') or None,
            chapters=b.get('chapters') or None,
        )
        added.append({"title": book.title, "id": book.id})

    return JsonResponse({"added": added, "skipped": skipped})

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

