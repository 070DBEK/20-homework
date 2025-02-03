from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.hashers import make_password
from .models import User
from .forms import UserForm


# 🔹 ListView - Barcha foydalanuvchilarni ko‘rsatish
class UserListView(View):
    template_name = "users/users.html"

    def get(self, request):
        users = User.objects.all()
        return render(request, self.template_name, {"users": users})


# 🔹 CreateView - Yangi foydalanuvchi qo‘shish
class UserCreateView(View):
    template_name = "users/users-form.html"

    def get(self, request):
        form = UserForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data["pass_1"])  # Parolni shifrlash
            user.save()
            return redirect("users:list")
        return render(request, self.template_name, {"form": form})


# 🔹 UpdateView - Foydalanuvchini tahrirlash
class UserUpdateView(View):
    template_name = "users/users-form.html"

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = UserForm(instance=user)
        return render(request, self.template_name, {"form": form})

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            if form.cleaned_data.get("pass_1"):  # Agar parol o'zgartirilgan bo'lsa
                user.password = make_password(form.cleaned_data["pass_1"])
            user.save()
            return redirect("users:list")
        return render(request, self.template_name, {"form": form})


# 🔹 DeleteView - Foydalanuvchini o‘chirish
class UserDeleteView(View):
    template_name = "users/users-delete-confirm.html"

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        return render(request, self.template_name, {"user": user})

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return redirect("users:list")
