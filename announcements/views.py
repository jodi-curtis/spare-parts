from django.shortcuts import render, redirect, get_object_or_404
from .models import Announcements
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import redirect_to_login
from django.urls import reverse_lazy

# Create your views here.
class AnnouncementsListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Announcements
    context_object_name = 'announcements'
    #Order anouncements by timestamp descending
    ordering = ['-timestamp']

    def get_queryset(self):
        return super().get_queryset()

    def post(self, request, *args, **kwargs):
        #Get id of announcement
        announcement_id = request.POST.get("announcement_id")
        #Get announcement where id is selected 
        announcement = get_object_or_404(Announcements, pk=announcement_id)
        #Update visible status to the oposite of what it already is
        announcement.visible = not announcement.visible
        announcement.save()

        #Set success messages
        if announcement.visible:
            messages.success(request, "Announcement is now visible.")
        else:
            messages.success(request, "Announcement has been hidden.")

        #Redirect back to announcments page
        return redirect('announcements')
    
    def test_func(self):
        return self.request.user.profile.user_group == 'store_manager'
    
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.warning(self.request, "You do not have permission to access the Announcements section")
            return redirect('login-success')
        else:
            messages.warning(self.request, "Login to access this page")
            return redirect_to_login(self.request.get_full_path())
        

class AnnouncementsCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Announcements
    #Announcment form should allow setting of message
    fields=['message']

    def form_valid(self, form):
        form.instance.posted_by = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('announcements')
    
    def test_func(self):
        return self.request.user.profile.user_group == 'store_manager'
    
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.warning(self.request, "You do not have permission to access the Announcements section")
            return redirect('login-success')
        else:
            messages.warning(self.request, "Login to access this page")
            return redirect_to_login(self.request.get_full_path())

class AnnouncementsUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Announcements
    #Announcment form should allow updating of message
    fields=['message']

    def form_valid(self, form):
        form.instance.posted_by = self.request.user
        return super().form_valid(form)
    
    #Only allow user who created announcment to update it
    def test_func(self):
        announcement = self.get_object()
        if self.request.user == announcement.posted_by:
            return True
        return False
    
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.warning(self.request, "You do not have permission to edit this announcement")
            return redirect('announcements')
        else:
            messages.warning(self.request, "Login to access this page")
            return redirect_to_login(self.request.get_full_path())
        
class AnnouncementDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Announcements
    success_url = reverse_lazy('announcements')
    
    #Only allow user who created announcment to delete it
    def test_func(self):
        announcement = self.get_object()
        if self.request.user == announcement.posted_by:
            return True
        return False
    
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.warning(self.request, "You do not have permission to delete this announcement")
            return redirect('announcements')
        else:
            messages.warning(self.request, "Login to access this page")
            return redirect_to_login(self.request.get_full_path())