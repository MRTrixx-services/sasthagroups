from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages

def home(request):
    return render(request, 'mobiles/home.html')

def mobiles(request):
    return render(request, "mobileshop/mobiles.html")


# ================================================================
#  mobiles/views.py  — add the contact_view function here
#  (keep all your existing views, just add this below them)
# ================================================================



# ── If you want to save enquiries to the database ──
# Uncomment the import below after adding ContactEnquiry to models.py
# from .models import ContactEnquiry


def contact_view(request):
    """
    Handles the Contact Us page for all three shops.
    GET  → shows the blank form
    POST → validates, saves to DB (optional), shows success message
    """

    # ── POST: process the submitted form ──
    if request.method == 'POST':
        name    = request.POST.get('name', '').strip()
        phone   = request.POST.get('phone', '').strip()
        email   = request.POST.get('email', '').strip()
        shop    = request.POST.get('shop', 'general').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()

        # ── Basic validation ──
        errors = []
        if not name:
            errors.append('Please enter your name.')
        if not phone:
            errors.append('Please enter your WhatsApp number.')
        if not subject:
            errors.append('Please select a subject.')
        if not message:
            errors.append('Please write a message.')

        if errors:
            # Re-render the form with error messages and keep the user's input
            for error in errors:
                messages.error(request, error)
            return render(request, 'mobiles/contact.html', {
                'form_data': request.POST,   # repopulate the form fields
            })

        # ── Save to database (uncomment after adding the model) ──
        # ContactEnquiry.objects.create(
        #     name    = name,
        #     phone   = phone,
        #     email   = email,
        #     shop    = shop,
        #     subject = subject,
        #     message = message,
        # )

        # ── Success: show message and redirect to the same page ──
        messages.success(
            request,
            f"Thank you {name}! We've received your message and will WhatsApp you shortly. 🌸"
        )
        return redirect('contact')   # PRG pattern: prevents duplicate submissions on refresh

    # ── GET: show the empty form ──
    return render(request, 'mobiles/contact.html', {
        'form_data': {},   # empty dict so template {{ form_data.name|default:'' }} doesn't error
    })