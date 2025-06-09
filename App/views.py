from django.shortcuts import render, redirect
from .models import song
from django.core.paginator import Paginator
from django.db.models import Q 


# Create your views here.
def index(request):
    paginator=Paginator(song.objects.all(),1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context= {
        'page_obj': page_obj,
    }
    return render(request, 'index.html', context)

def home(request):
    return render(request, 'home.html')

from django.core.paginator import Paginator

from django.db.models import Q

def dashboard(request):
    query = request.GET.get('q')  # get the search query from URL ?q=searchterm
    if query:
        song_list = song.objects.filter(
            Q(title__icontains=query) | Q(artist__icontains=query)
        )
    else:
        song_list = song.objects.all()

    paginator = Paginator(song_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,  # pass the current search term to template
    }
    return render(request, 'dashboard.html', context)



def upload_song(request):
    if request.method == 'POST':
        form = songForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('music-player')  # change to your music player view name
    else:
        form = songForm()
    return render(request, 'upload_song.html', {'form': form})

def main_view(request):
    songs = song.objects.all().order_by('-id')
    paginator = Paginator(songs, 5)  # 5 songs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'main.html', {'page_obj': page_obj})


