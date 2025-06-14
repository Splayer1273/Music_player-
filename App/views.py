from django.shortcuts import render, redirect
from .models import Song
from django.core.paginator import Paginator
from django.db.models import Q 
from .forms import SongForm
from django.contrib import messages

# Create your views here.
def index(request):

    paginator=Paginator(Song.objects.all(),1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context= {
        'page_obj': page_obj,
    }
    return render(request, 'index.html', context)

def home(request):
    return render(request, 'home.html')



def dashboard(request):
    query = request.GET.get('q')  # get the search query from URL ?q=searchterm
    if query:
        song_list = Song.objects.filter(
            Q(title__icontains=query) | Q(artist__icontains=query)
        )
    else:
        song_list = Song    .objects.all()

    paginator = Paginator(song_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,  # pass the current search term to template
    }
    return render(request, 'dashboard.html', context)



# def upload_song(request):
#     if request.method == 'POST':
#         form = SongForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('music-player')  # change to your music player view name
#     else:
#         form = SongForm()
#     return render(request, 'upload_song.html', {'form': form})

def main_view(request):
    songs = Song.objects.all().order_by('-id')
    paginator = Paginator(songs, 5)  # 5 songs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'main.html', {'page_obj': page_obj})

def add_song(request):
    if request.method == 'POST':
        form = SongForm(request.POST, request.FILES)
        if form.is_valid():
            # Extract the cleaned data for comparison
            title = form.cleaned_data.get('title')
            artist = form.cleaned_data.get('artist')

            # Check if a song with the same title and artist already exists
            if Song.objects.filter(title=title, artist=artist).exists():
                messages.error(request, 'This song already exists!')
            else:
                form.save()
                messages.success(request, 'Song added successfully!')
                return redirect('/dashboard/')  # Or redirect to song list
        else:
            messages.error(request, 'Failed to add song. Please correct the errors.')
    else:
        form = SongForm()
    return render(request, 'add_song.html', {'form': form})

def about_us(request):
    return render(request, 'about_us.html')