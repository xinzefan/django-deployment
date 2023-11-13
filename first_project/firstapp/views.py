from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect , HttpResponse
from django.contrib.auth import authenticate,login,logout
from firstapp.forms import UserForm, UserProfileInfoForm
# connect to db
# from firstapp.models import Topic,AccessRecord,Webpage,User
# Create your views here.
def index(request):
    context = {
        'text' : "hello world",
        'number' : 100
    }

    return render(request,'firstapp/index.html',context=context)

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))
@login_required
def special(request):
    return HttpResponse("you are logged in")

def register(request):
    registered=False
    if request.method =="POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user 
            if "profile_pic" in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request, "firstapp/registration.html",
                  context={'user_form':user_form, 'profile_form' : profile_form, 'registered': registered})

def user_login(request):

    if request.method == 'POST':
        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)

        # If we have a user
        if user:
            #Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request,user)
                # Send the user back to some page.
                # In this case their homepage.
                return HttpResponseRedirect(reverse('index'))
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    else:
        #Nothing has been provided for username or password.
        return render(request, 'firstapp/login.html', {})

# def other(request):

#     return render(request,'firstapp/other.html')

# def relative(request):

#     return render(request,'firstapp/relative_url_templates.html')

# def users(request):
#     form = NewUserForm()
#     if request.method == "POST":
#         form = NewUserForm(request.POST)

#         if form.is_valid():
#             form.save(commit=True)
#             return index(request)
#         else:
#             print("form invalid")
#     return render(request,'firstapp/user.html',{'form':form})


# def form_name_view(request):
#     form = forms.FormName()

#     if request.method == 'POST':
#         form = forms.FormName(request.POST)
#         if form.is_valid():
#             print("validatation work")
#             print(form.cleaned_data['name'])

#     return render(request, 'firstapp/form_page.html',{'form':form})

# def user(request):
#     # webpages_list = AccessRecord.objects.order_by('date')
#     # date_dic= {
#     #     'access_record' : webpages_list
#     # }
#     # return render(request, "firstapp/index.html", context=date_dic)
#     user_list = User.objects.order_by('first_name')
#     user_dic = {
#         'users' : user_list
#     }
#     return render(request, "firstapp/user.html", context=user_dic)

# def help(request):
#     my_dict = {
#         'help_me' : "Help Page"
#     }
#     return render(request, 'firstapp/index.html',context=my_dict)
