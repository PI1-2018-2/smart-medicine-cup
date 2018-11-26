from django.shortcuts import render
from django.views.generic import ListView, TemplateView, CreateView, FormView, View
from django.utils.decorators import method_decorator

# Local Django imports
from cups.models import Cup, Record, Contact
from cups.forms import CupForm

class Dashboard(View):
    """
    Renders the home page (dashboard) of the health professional.
    """
    template_name = 'dashboard.html'


    def dispatch(self, *args, **kwargs):
        return super(Dashboard, self).dispatch(*args, **kwargs)

    def get(self, request):

        # Set initial date first hour
        list_record = Record.objects.all()

        # Get six latest prescriptions
        list_cups = Cup.objects.filter(user_id=self.request.user)

        return render(request, self.template_name, {'list_record': list_record,
                                                    'list_cups': list_cups})



class EditRegistration(TemplateView):
    template_name = "edit_registration.html"

class Login(TemplateView):
    template_name = "login.html"

class Contacts(ListView):
    template_name = "contacts.html"
    context_object_name = 'list_contacts'
    model = Contact
    ordering = ['-date_created']

    def dispatch(self, *args, **kwargs):
        return super(Contacts, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

class AddSmc(FormView):
    template_name = "addsmc.html"
    form_class = CupForm
    success_url = '/dashboard/smc'
    def dispatch(self, *args, **kwargs):

        return super(AddSmc, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.cup = form.save(commit=False)
        self.cup.user_id = self.request.user.id
        self.cup.save()

        return super(AddSmc, self).form_valid(form)


class Smc(ListView):
    template_name = "smc.html"
    context_object_name = 'list_cups'
    model = Cup
    ordering = ['-date_created']

    def dispatch(self, *args, **kwargs):
        return super(Smc, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

class Historic(ListView):
    template_name = "historic.html"
    context_object_name = 'list_record'
    model = Record 
    ordering = ['-date_created']

    def dispatch(self, *args, **kwargs):
        return super(Historic, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        query = Cup.objects.filter(user=self.request.user)
        print(self.model.objects.all())
        return self.model.objects.all()
