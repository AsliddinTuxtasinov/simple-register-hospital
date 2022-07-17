from django.contrib.auth import authenticate, login
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView, CreateView, DetailView, ListView, UpdateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .models import DiseasedUser, SpecialDoctor, StatusDiseasedUser
from .forms import (
    CreateDiseasedForm, CreateDoctorForm,
    FilterForm, LoginForm, UpdateDiseasedForm,
    StatusDiseasedUserForm
)


class IndexView(TemplateView):
    template_name = "index.html"


class AdminDashboardView(ListView, LoginRequiredMixin):
    template_name = "admin_dashboard.html"
    model = DiseasedUser
    context_object_name = 'objects'
    paginate_by = 4
    paginate_orphans = 1

    def get_queryset(self):

        if self.request.user.is_doctor:
            doctors = SpecialDoctor.objects.get(pk=self.request.user.pk)
        else:
            doctors = None
        queryset = super().get_queryset().filter(type_of_doctors=doctors, is_doctor_view=False)
        queryset = FilterForm(self.request.GET, queryset=queryset)
        return queryset.qs

    def get_context_data(self, *args, **kwargs):
        try:
            context = super().get_context_data()
        except Http404:
            self.kwargs['page'] = 1
            context = super().get_context_data()

        context['is_doctor'] = self.request.user.is_authenticated and self.request.user.is_doctor
        context['filter_form'] = FilterForm(self.request.GET, queryset=self.get_queryset())
        return context


class CreateDiseasedView(CreateView):
    template_name = "register.html"
    form_class = CreateDiseasedForm
    success_url = None

    def form_valid(self, form):
        self.object = form.save()
        url = self.object
        self.success_url = url.get_absolute_url

        messages.success(request=self.request, message="successfully completed")
        return super().form_valid(form)

    def get_success_url(self):
        if self.success_url:
            url = self.object.get_absolute_url()
        else:
            messages.error(self.request, 'something is error, please check it')
            url = reverse_lazy("register")
        return url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_register'] = True
        return context


class GotoDoctorView(UpdateView):
    model = DiseasedUser
    form_class = UpdateDiseasedForm
    template_name = "register.html"
    success_url = reverse_lazy("profile")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_goto_doctor'] = True
        return context


class CreateDoctorView(CreateView, LoginRequiredMixin):
    model = SpecialDoctor
    template_name = "register.html"
    success_url = reverse_lazy("profile")
    form_class = CreateDoctorForm

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save(commit=False)
        self.object.is_doctor = True
        self.object.set_password(form.cleaned_data.get("password"))
        self.object.save()
        messages.success(request=self.request, message="successfully completed")
        return super().form_valid(form)


class DetailPageView(DetailView):
    model = DiseasedUser
    context_object_name = 'obj'
    template_name = 'detail_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action_form'] = StatusDiseasedUserForm()
        context['is_doctor'] = self.request.user.is_authenticated and self.request.user.is_doctor
        return context


class CreateStatusDiseasedUserView(CreateView):
    model = StatusDiseasedUser
    form_class = StatusDiseasedUserForm
    success_url = reverse_lazy("profile")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        diseased = get_object_or_404(DiseasedUser, pk=self.kwargs['diseased_id'])
        doctor = get_object_or_404(SpecialDoctor, pk=self.request.user.pk)

        self.object.diseased = diseased
        self.object.doctor = doctor
        self.object = form.save(commit=True)

        diseased.is_doctor_view = True
        diseased.save()
        return super().form_valid(form)


class LoginView(View):

    def get(self, request):
        login_form = LoginForm()
        return render(request, "login.html", {"login_form": login_form})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            tel_number = login_form.cleaned_data.get('tel_number')
            password = login_form.cleaned_data.get('password')
            user = authenticate(tel_number=tel_number, password=password)
            if user:
                login(request, user)
                messages.info(request, "You are now successfully logged.")
                return redirect("profile")
        messages.error(request, "Invalid tel number or password.")
        return render(request, "login.html", {"login_form": login_form})


class LogoutView(LogoutView):
    pass
