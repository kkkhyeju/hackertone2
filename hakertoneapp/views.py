from django.shortcuts import render , redirect, get_object_or_404
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib import auth
from django.core.paginator import Paginator
from .models import Team,Profile,Question,Answer
from .form import CustomUserChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
import random
# Create your views here.

def signup(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            user = User.objects.create_user(username= request.POST['username'], password = request.POST['password1'])
            auth.login(request, user)
            return redirect('index')
    return render(request, 'login.html')

def login(request):
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(request, username=username , password = password)
            if user is not None and username == "kimhyeju":
                auth.login(request,user)
                return redirect('ad_page')
                #return render(request,'ad_page.html')
            elif user is not None:
                auth.login(request,user)
                return redirect('index')    
            else:
                errormasg = "잘못입력하셨습니다"
                return render(request, 'login.html',{'errormasg':errormasg})
        else:
            return redirect('login.html')

def logout(request):
    auth.logout(request)
    return render(request, 'login.html')


# def delete(request, account_id):
#         account = Account.objects.get(id=account_id)
#         account.delete()
#         return redirect('index')

def loginhome(request):
    return render(request,'login.html')


def get_random_code():
    password = ''
    for i in range(8):
        password += random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789')
    return password

def maketeam(request):
    questions=Question.objects
    questions_list = Question.objects.all()
    paginator = Paginator(questions_list,10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    group_code = get_random_code()
    return render(request,'maketeam.html',{"questions":questions, "posts":posts, "group_code": group_code})

def index(request):
    first = Question.objects.order_by("?")[0]
    myanswer = Answer.objects.filter(userName = request.user)
    return render(request,'index.html', {'first': first,'myanswer':myanswer})
    
def ad_page(request):
    questions = Question.objects
    return render(request,'ad_page.html',{'questions':questions})
    #return render(request,'ad_page.html')

def create(request):
    question = Question()
    question.title = request.GET['title']
    question.save()
    return redirect('ad_page')

def createteam(request):
    team=Team()
    team.teamname = request.POST['teamname']
    team.teamcode = request.POST['groupcode']
    team.howlong = request.POST['howlong']
    team.questionlist = dict(request.POST)['case[]']
    team.save()
    profile = Profile.objects.get(user = request.user)
    profile.team = request.POST['teamname']
    profile.teamcheck =True
    profile.save()
    return redirect('index')

def answer(request):
    answer = Answer()
    print(request.POST)
    answer.userName = request.user
    answer.question = request.POST['question']
    answer.answerlist = request.POST['fulltext']
    answer.save()

    return redirect('index')

#def search(request):
#    searchteam=Team.objects.filter(teamname=request.POST['filter'])
#    if searchteam is not None:
#        result = searchteam
#        return render(request,'maketeam.html',{'result':result})
#    else:
#        return render(request,'maketeam.html')

def update(request):
    if request.method == "POST":
    	# updating
        user_change_form = CustomUserChangeForm(data=request.POST, instance=request.user)
        
        if user_change_form.is_valid():
            user = user_change_form.save()
        return redirect('index')

    else:
        # editting
        user_change_form = CustomUserChangeForm(instance=request.user)

        context = {
            'user_change_form': user_change_form,
        }
        
        return render(request, 'update.html', context)

def change_pw(request):
    if request.method == "POST":
        password_change_form = PasswordChangeForm(request.user, request.POST)
        
        if password_change_form.is_valid():
            user = password_change_form.save()
            update_session_auth_hash(request, user)

            return redirect('index')
        
    else:
        password_change_form = PasswordChangeForm(request.user)

    return render(request, 'change_pw.html', {'password_change_form':password_change_form})

    
def team_in(request):    
    context= {}
    if request.method == 'POST':
        invitecode = request.POST.get('invitecode')
        if Team.objects.filter(teamcode = invitecode) :
            #if invitecode:
            curr_team = Team.objects.get(teamcode = invitecode)
            profile = Profile.objects.get(user = request.user)
            user = request.user.username
            #print(user)
            curr_team.userlist =curr_team.userlist + ','+ user
            curr_team.save()
            profile.team = curr_team.teamname
            profile.teamcheck =True
            profile.save()
            #return redirect(request,'index.html',{'teamlist':curr_team.userlist})
            return render(request,'index.html',{'teamlist':curr_team.userlist})
        else :
            context.update({'error':"해당 팀이 존재하지 않습니다."})
            return render(request, 'index.html')