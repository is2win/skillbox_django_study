from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from .forms import UserBioForm, UploadFileForm


# Create your views here.
def process_get_view(request: HttpRequest) -> HttpResponse:
    a = request.GET.get('a', '')
    b = request.GET.get('b', '')
    result = a + b
    context = {
        'a': a,
        'b': b,
        'result': result,
    }
    return render(request, 'requestdataapp/request-query-params.html', context=context)


def user_form(request: HttpRequest) -> HttpResponse:
    context = {
        "form": UserBioForm()
    }
    return render(request, 'requestdataapp/user-bio-form.html', context=context)


def handle_file_upload(request: HttpRequest) -> HttpResponse:

    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # my_file = request.FILES["myfile"]
            my_file = form.cleaned_data["file"]
            fs = FileSystemStorage()
            file_name = fs.save(my_file.name, my_file)
            print("saved file:", file_name)
    else:
        form = UploadFileForm()
    context = {
        "form": form,
    }
    return render(request, 'requestdataapp/file-upload.html', context=context)