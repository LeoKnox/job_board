from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
import bcrypt
from.models import Helper, Job
# Create your views here.
def index(request):
    return render(request, "job_app/index.html")

def register(request):
    errors = Helper.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.erro(request, value)
        return redirect('/')
    else:
        hpwd = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        Helper.objects.create(first_name=request.POST["fname"],last_name=request.POST["lname"],password=hpwd,email=request.POST["email"])
        request.session['use'] = request.POST["fname"]
        return redirect("/board")

def login(request):
    errors = Helper.objects.pw_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        name = Helper.objects.filter(email=request.POST["email"])
        request.session['use'] = name[0].first_name
        return redirect("/board")

def board(request):
    if 'use' not in request.session:
        return redirect("/")
    context = {
        "jobs":Job.objects.all()
    }

    return render(request,"job_app/board.html", context)

def new_job(request):

    return render(request,"job_app/new_job.html")

def create_job(request):
    errord = Helper.objects.job_validator(request.POST)
    if len(errord) > 0:
        for key, value in errord.items():
            messages.error(request, value)
        return redirect("/new_job")
    id = Helper.objects.get(first_name=request.session['use'])
    print(id.id)
    Job.objects.create(job=request.POST['njob'], description = request.POST['ndescription'], location = request.POST['nlocation'], creator=id)

    return redirect('/board')