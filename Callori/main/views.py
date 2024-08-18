from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template.loader import get_template
from django.template import TemplateDoesNotExist
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.views.generic.edit import UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from .models import User, Posted
from .forms import ProfileEditForm, AIFormSet, PostedForm
from django.views.generic.edit import CreateView
from .forms import RegisterForm
from django.views.generic.base import TemplateView
from django.core.signing import BadSignature
from .utilities import signer
from django.views.generic.edit import DeleteView
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import redirect

# Вход на главную страницу
def index(request):
    bbs = Posted.objects.filter(is_active=True)[:10]
    context = {'bbs': bbs}
    return render(request, 'main/index.html', context)
# Открытие других страниц
def other_page(request, page):
    try:
        template = get_template('main/' + page + '.html')
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))
# Регистрация
class BBLogin_View(LoginView):
    template_name = 'main/login.html'

# Выход
class BBLogout_View(LogoutView):
    pass
# Профиль
@login_required()
def profile(request):
    bbs = Posted.objects.filter(author=request.user.pk)
    context = {'bbs': bbs}
    return render(request, 'main/profile.html', context)
# Изменения дааных пользователя кроме пароля
class ProfileEditView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'main/profile_edit.html'
    form_class = ProfileEditForm
    success_url = reverse_lazy('main:profile')
    success_message = 'Данные пользователя изменены'
    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)
    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
            return get_object_or_404(queryset, pk=self.user_id)
# Изменение пароля
class PasswordEditView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'main/password_edit.html'
    success_url = reverse_lazy('main:profile')
    success_message = 'Пароль пользователя изменен'
# Страница Регистрации
class RegisterView(CreateView):
    model = User
    template_name = 'main/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('main:register_done')

# Страница об успешной авторизации
class RegisterDoneView(TemplateView):
 template_name = 'main/register_done.html'

# Активация нового пользователя
def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'main/activation_failed.html')
    user = get_object_or_404(User, username=username)
    if user.is_activated:
        template = 'main/activation_done_earlier.html'
    else:
        template = 'main/activation_done.html'
    user.is_active = True
    user.is_activated = True
    user.save()
    return render(request, template)

# Удаление пользователя
class ProfileDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'main/profile_delete.html'
    success_url = reverse_lazy('main:index')
    success_message = 'Пользователь удален'
    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        logout(request)
        return super().post(request, *args, **kwargs)
    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)

def blog(request):
    bbs = Posted.objects.filter(is_active=True)[:10]
    context = {'bbs': bbs}
    return render(request, 'main/blog.html', context)

def posted_detail(request, pk):
    return render(request, 'main/posted_detail.html', context={'bb': get_object_or_404(Posted, pk=pk)})

@login_required
def profile_posted_add(request):
    if request.method == 'POST':
        form = PostedForm(request.POST, request.FILES)
        if form.is_valid():
            bb = form.save()
            formset = AIFormSet(request.POST, request.FILES, instance=bb)
            if formset.is_valid():
                formset.save()
                messages.add_message(request, messages.SUCCESS,'Объявление добавлено')
                return redirect('main:profile')
    else:
        form = PostedForm(initial={'author': request.user.pk})
        formset = AIFormSet()
    context = {'form': form, 'formset': formset}
    return render(request, 'main/profile_posted_set.html', context)