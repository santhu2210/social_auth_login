from django.shortcuts import render

# Create your views here.
from django.views import generic
from django.views.generic import View
from django.contrib.auth import authenticate, logout, get_user_model, login
from django.views.generic.edit import UpdateView

from django.shortcuts import render_to_response, redirect, render, get_object_or_404
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
# from django.template.context import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from  .forms import LoginForm, DetailForm
from django.template.loader import render_to_string
from django.core.mail import send_mail


class LoginView(generic.FormView):
    form_class = LoginForm
    success_url = '/'
    template_name = 'registration/login.html'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        uri = '/profile/user/'
        if user is not None and user.is_active:
            login(self.request, user)

            if not user.is_staff:
                if self.request.GET.get('next') is not None and self.request.GET.get('next') != '':
                    uri = uri + '?next=' + self.request.GET.get('next')
                return redirect(uri)

            if self.request.GET.get('next') is not None and self.request.GET.get('next') != '':
                return redirect(self.request.GET.get('next'))

            return super(LoginView, self).form_valid(form)
        else:
            User = get_user_model()
            print User._meta.fields

            if User.objects.filter(email=username).exists():
                exist_user = authenticate(username=username, password=password)
                print exist_user
                if exist_user is None:
                    form.add_error("username", "user name and password is mismatch")
                    return self.form_invalid(form)

                form.add_error("username", "Username is already taken try with new username")
                return self.form_invalid(form)
            # print username, password

            created = User.objects.create_user(email=username, username=username, password=password)
            # print type(created)

            if created:
                user = authenticate(username=username, password=password)
                print user
                login(self.request, user)

                # check if user has any pending invites
                # pendingAccess = AccessPending.objects.filter(email=user.email)
                # for pending in pendingAccess:
                #     wishlist = pending.wish_id
                #     access_model = Access
                #     try:
                #         obj = access_model.objects.get(user_id=user.id, wish=wishlist)
                #     except access_model.DoesNotExist:
                #         obj = access_model(user=user, wish_id=wishlist)
                #         obj.save()

                #     # delete
                #     instance = AccessPending.objects.get(id=pending.id)
                #     instance.delete()

                if not user.is_staff:
                    if self.request.GET.get('next') is not None and self.request.GET.get('next') != '':
                        uri = uri + '?next=' + self.request.GET.get('next')
                    return redirect(uri)

                if self.request.GET.get('next') is not None and self.request.GET.get('next') != '':
                    return redirect(self.request.GET.get('next'))

                return super(LoginView, self).form_valid(form)
            else:
                return self.form_invalid(form)


# def login(request):
#     # context = RequestContext(request, {
#     #     'request': request, 'user': request.user})
#     # return render_to_response('login.html', context_instance=context)
#     return render(request, 'login.html')

@login_required(login_url='login')
def is_inducted(request):
    user = request.user
    uri = '/profile/user/'
    if not user.is_staff:
        return redirect(uri)
    else:
        return redirect('/home')

def send_invite_mail(template, title, recipients):
    msg_html = template
    try:
        send_mail(
            title,
            msg_html,
            'no-reply@techaffinity.com',
            recipients,
            html_message=msg_html,
        )

    except Exception as e:
        print e
        print 'mail sending failed'


class InductionView(UpdateView):
    form_class = DetailForm
    model = User
    template_name = 'registration/user_detail.html'

    def get_object(self):
        return get_object_or_404(get_user_model(), pk=self.request.user.id)

    def form_valid(self, form):
        user = self.request.user
        # country = form.cleaned_data['country']
        # user.country = country

        if form.cleaned_data['first_name']:
            user.first_name = form.cleaned_data['first_name']

        if form.cleaned_data['last_name']:
            user.last_name = form.cleaned_data['last_name']

        user.is_staff = True
        user.save()

        # kick off welcome mail
        username = user.email
        if form.cleaned_data['first_name']:
            username = form.cleaned_data['first_name']
        email_data = {
            'user_fname': username
        }
        email_template = render_to_string('welcome_email.html', email_data)
        send_invite_mail(email_template, 'Welcome to New Community', [user.email])

        if self.request.GET.get('next') is not None and self.request.GET.get('next') != '':
            return redirect(self.request.GET.get('next'))

        return redirect('/')



@login_required(login_url='/')
def home(request):
    return render_to_response('home.html')


def logout(request):
    auth_logout(request)
    return redirect('/')
