from django.shortcuts import render, redirect
from django.views import View 
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth.models import User 
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from home.models import Post
from django.contrib.auth import views as auth_view
from django.urls import reverse_lazy
from accounts.models import Relation


class UserRegisterView(View):
    """CBV for registering user"""
    
    form_class     = UserRegisterForm
    template_class = 'accounts/register.html'
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        else:
            return super().dispatch(request, *args, **kwargs)
        
    def get(self, request):
        user_form = self.form_class()
        
        return render(request, self.template_class, {'user_form':user_form}) 
    
    def post(self, request):
        user_form = self.form_class(request.POST)
        if user_form.is_valid():
            cd = user_form.cleaned_data
            User.objects.create_user(cd['username'], cd['email'], cd['password'])
            messages.success(request, f"Hi Dear {cd['username']} ! Your account was created successfuly!",'success')
        
            return redirect('home:home')
        
        return render(request, self.template_class, {'user_form':user_form})
    
    
class UserLoginView(View):
    """CBV for Login user"""
        
    form_class     = UserLoginForm
    template_class = 'accounts/login.html'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        else:
            return super().dispatch(request, *args, **kwargs)
    def setup(self, request, *args , **kwargs):
        """saving 'next' in url for redirect to wanted profile (if exsits) after login"""
        self.next = request.GET.get('next')
        return super().setup(request, *args , **kwargs)
               
    def get(self, request):
        user_form = self.form_class()
        return render(request, self.template_class, {'user_form':user_form}) 
    
    def post(self, request):
        user_form = self.form_class(request.POST)
        if user_form.is_valid():
            cd = user_form.cleaned_data
            user = authenticate(request, username=cd['username'],password= cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, f"Hi Dear {cd['username']} ! You have logged in successfuly!",'success')
                if self.next:
                    return redirect(self.next)
                return redirect('home:home')
                
            messages.error(request, "Wrong username or password!",'error')

        return render(request, self.template_class, {'user_form':user_form})
    
    
class UserLogoutView(LoginRequiredMixin, View):
    """CBV for Loging out user""" 
        
    def get(self, request):
        logout(request)
        messages.success(request, f"You have logged out successfuly!ByeBye!",'success')
        return redirect('home:home')
 
            
class UserProfileView(LoginRequiredMixin, View):
    """CBV for user profile""" 
        
    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        posts = Post.objects.filter(user=user)
        
        is_following = False
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            is_following = True
        return render(request, 'accounts/profile.html/',
                      {'user':user, 'posts':posts, 'is_following':is_following})
    

# Forgotten Password!___________________________________________________
class UserPasswordResetView(auth_view.PasswordResetView):
    """ view for reseting password"""
    template_name = 'accounts/password_reset_form.html'
    success_url   = reverse_lazy('accounts:password_reset_done')
    email_template_name = 'accounts/password_reset_email.html'
    
    
class UserPasswordResetDoneView(auth_view.PasswordResetDoneView):
    """view for finishing resetting of pass"""
    template_name = 'accounts/password_reset_done.html'
    
    
class UserPasswordResetConfirmView(auth_view.PasswordResetConfirmView):
    """confirming new pass"""
    template_name = 'accounts/password_reset_confirm.html'
    success_url   = reverse_lazy('accounts:password_reset_complete')
    

class UserPasswordResetCompleteView(auth_view.PasswordResetCompleteView):
    """ reseting pass is completed"""
    template_name = 'accounts/password_reset_complete.html'
    
# following ___________________________________________________________
class UserFollowView(LoginRequiredMixin, View):
    """ following"""
    def get(self, request, user_id ):
        user = User.objects.get(id=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            messages.error(request, "You already follow this user!",'error')
        else:
            Relation(from_user=request.user, to_user=user).save()
            messages.success(request, f"You are follower of {user} from now!",'success')
        return redirect('accounts:user_profile', user_id)

class UserUnFollowView(LoginRequiredMixin, View):
    """ unfollowing"""
    def get(self, request, user_id ):
        user = User.objects.get(id=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            relation.delete()
            messages.success(request, f"You have unfollowed {user}!",'success')
        else:
            messages.error(request, "for unfollow users you should had followed them before!!",'error')     
        
        return redirect('accounts:user_profile', user_id)

            