from django.contrib.auth.decorators import login_required

from ..models import Cup, Contact
from ..forms.cup import RegistrationCup


@login_required
def register_cup(request):
    if request.method == 'POST':
        form = RegistrationCup(request.POST)
        if form.is_valid():
            form.save()
            code = request.POST.get('code')
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            if not exist(Cup(code)):
                contact = Contact(name=name, phone=phone, email=email)
                contact.save()

            elif cup.is_activated()
                cup = Cup(cup.user.add(user), contact=contact.primary_key)
                cup.save()
            return redirect('/dashboard/')
    else:
        form = RegistrationCup()
    return redirect('/dashboard/')
