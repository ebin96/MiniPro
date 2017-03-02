from django.shortcuts import render,redirect,get_object_or_404,HttpResponse,HttpResponseRedirect
from django.views import View
from accounts.admin import UserCreationForm
from django.contrib.auth import authenticate, login ,logout
from .forms import ProfileForm,TestForm
from accounts.forms import LoginForm
from django.contrib.auth import get_user_model
from .models import Profile
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.http import JsonResponse
from tests.models import Apt_Test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import pdb
from django.urls import reverse ,reverse_lazy
user =get_user_model()
# Create your views here.
class Indexpage(View):
    template_name='index.html'
    def get(self, request, *args):
        form=LoginForm()
        return render(request,self.template_name,{"form":form})
    def post(self,request, *args):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('/home/')
        return render(request, self.template_name, {"form": form})
class Registerpage(View):
    template_name='register.html'
    def get(self, request, *args):

        form=UserCreationForm()
        profile=ProfileForm()
        context={
            "form":form,
            "profile":profile,
        }
        return render(request,self.template_name,context)

    def post(self, request, *args):
        form = UserCreationForm(request.POST)
        profile = ProfileForm(request.POST,request.FILES)
        context = {
            "form": form,
            "profile":profile,

        }


        if form.is_valid() and profile.is_valid():
            user = form.save()
            pro= profile.save(commit=False)

            pro.user=user
            pro.slug=slugify(pro.name)
            pro.save()
            if pro is not None:
                login(request,user)
                return redirect('/home/')

        return render(request, self.template_name, context)
class Homepage(View):
    template_name='home.html'
    tctemplate='tcpc.html'
    def get(self,request,*args):
        if not request.user.is_authenticated:
            return redirect(reverse("accounts:index"))
        p=Profile.objects.get(user=request.user)

        if p.status != 'ST':
            return render(request,self.tctemplate,{})
        #paginatior code these contacts are really tests im too lazy to change the names
        contact_list = Apt_Test.objects.all()
        paginator = Paginator(contact_list, 25)
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            contacts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            contacts = paginator.page(paginator.num_pages)

        return render(request,self.template_name,{"profile":p,'contacts': contacts})
class createtest(View):
    createtestt="createtest.html"
    def get(self,request):
        return render(request,self.createtestt,{"tform":TestForm()})
def logoutview(request):
    logout(request)
    return redirect('/')
    from django.contrib.auth.decorators import login_required

@login_required(redirect_field_name='redirecting',login_url='')

def profileview(request,slug):
    p = Profile.objects.get(slug=slug)
    return render(request,'profile.html',{"profile":p})



def validate_username(request):
    username = request.GET.get('name', None)
    data = {
        'is_taken': Profile.objects.filter(name__iexact=username).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'A user with this username already exists.'
    return JsonResponse(data)
