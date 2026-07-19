from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone

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
        #     name=name, phone=phone, email=email,
        #     shop=shop, subject=subject, message=message,
        # )

        # ── Send email notification ──
        subject_labels = {
            'price_inquiry': 'Price Inquiry',
            'appointment':   'Book Appointment',
            'order':         'Place an Order',
            'complaint':     'Complaint / Feedback',
            'wholesale':     'Wholesale / Bulk',
            'other':         'Other',
        }
        shop_labels = {
            'mobile':  'Mobile Shop',
            'parlour': 'Beauty Parlour',
            'flower':  'Flower Shop',
            'general': 'General',
        }
        ctx = {
            'name':            name,
            'phone':           phone,
            'email':           email,
            'shop':            shop,
            'shop_display':    shop_labels.get(shop, 'General'),
            'subject_display': subject_labels.get(subject, subject),
            'message':         message,
            'submitted_at':    timezone.now().strftime('%d %b %Y, %I:%M %p'),
        }
        # ── Admin notification email ──
        admin_html = render_to_string('mobiles/email/contact_email.html', ctx)
        admin_subject = f"[Sastha Group] New {ctx['shop_display']} Enquiry from {name}"
        admin_msg = EmailMultiAlternatives(
            subject=admin_subject,
            body=f"New enquiry from {name} ({phone}) — {ctx['subject_display']}\n\n{message}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=['info@sasthagroup.com'],
            reply_to=[email] if email else [],
        )
        admin_msg.attach_alternative(admin_html, 'text/html')

        # ── User confirmation email (only if they gave an email) ──
        if email:
            user_html = render_to_string('mobiles/email/contact_email_user.html', ctx)
            user_msg = EmailMultiAlternatives(
                subject="We received your message – Sastha Group 🌸",
                body=f"Hi {name}, thank you for contacting Sastha Group! We've received your enquiry and will WhatsApp you at {phone} shortly.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[email],
            )
            user_msg.attach_alternative(user_html, 'text/html')

        try:
            admin_msg.send()
            if email:
                user_msg.send()
        except Exception:
            pass  # don't block the user if email fails

        # ── Success: show message and redirect to the same page ──
        messages.success(
            request,
            f"Thank you {name}! We've received your message and will WhatsApp you shortly. 🌸"
        )
        return redirect('contact')

    # ── GET: show the empty form ──
    return render(request, 'mobiles/contact.html', {
        'form_data': {},   # empty dict so template {{ form_data.name|default:'' }} doesn't error
    })