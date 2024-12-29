from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from .models import RSVP
import qrcode
import os
from dotenv import load_dotenv
from io import BytesIO
import base64


class RSVPform(forms.ModelForm):
    class Meta:
        model = RSVP
        fields = ['name', 'email', 'attending', 'partner'] # müssen drin sein, sonst IntegrityError

    # Name-Feld
    name = forms.CharField(
        widget=forms.TextInput(  # Statt CharInput verwenden wir TextInput
            attrs={"placeholder": "Vorname Nachname"}
        ),  # Platzhalter für das Name-Feld
        label="Name",
    )

    # Email-Feld
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"placeholder": "you@example.com"}
        ),  # Platzhalter für das Email-Feld
        label="Email",
    )

    # Teilnahme-Feld (BooleanField wird standardmäßig als Checkbox gerendert)
    attending = forms.BooleanField(label="Ich werde kommen:", required=False)
    partner = forms.BooleanField(label="Ich bringe meinen Partner mit:", required=False)

    child_1 = forms.BooleanField(label="Ich bringe 1 Kind:", required=False)
    child_2 = forms.BooleanField(label="Ich bringe 2 Kinder:", required=False)

    not_attending = forms.BooleanField(label="Ich werde nicht kommen:", required=False)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if RSVP.objects.filter(email=email).exists():
            raise forms.ValidationError("Hoppla, diese Email-Adresse wurde bereits registriert. Warst das nicht du? Wende dich gerne an website@nicostern.de :)")
        return email

    # def clean_negative(self):

    def clean(self):
        cleaned_data = super().clean()

        # child_1 und child_2: bool -> IntegerField
        child_1 = self.cleaned_data.get('child_1', False)
        child_2 = self.cleaned_data.get("child_2", False)
        if child_1 and child_2:
            raise forms.ValidationError(
                "Huch! Du hast ausgewählt, dass du sowohl 1 als auch 2 Kinder mitbringst. Sind die so schnell gewachsen? Bitte entscheide dich für eine Option – wir brauchen Klarheit!"
            )
        cleaned_data["kids"] = 1 if child_1 else 2 if child_2 else 0

        # Guard: not coming, but bringing guests???
        attending = self.cleaned_data.get("attending")
        partner = self.cleaned_data.get("partner")
        if not attending and (cleaned_data["kids"] != 0 or partner):
            raise forms.ValidationError(
                "Öhm, du hast angegeben, dass du nicht kommst, aber Gäste mitbringst? Das passt nicht so ganz: Bitte korrigiere das."
            )
            
        # Guard: coming, but not attending???
        if attending and self.cleaned_data.get("not_attending"):
            raise forms.ValidationError(
                "Du hast angegeben, dass du kommst, aber auch, dass du nicht kommst. Das ist sus. Bitte korrigiere das."
            )

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.kids = self.cleaned_data.get("kids")
        if commit:
            instance.save()
        return instance


def index(request):
    load_dotenv()

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # create QR code > img
    qr.add_data(os.getenv("DROPZONE_URL"))
    qr.make(fit=True)
    img = qr.make_image(fill_color="#A2836E", back_color="white")

    # QR Code -> Base64
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    qr_img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    buffer.close()

    if request.method == "POST":
        form = RSVPform(request.POST)
        if form.is_valid():
            form.save()  # speichert in DB
            return HttpResponse("Danke für deine Rückmeldung! Wenn diese Seite immer noch nur eine hässliche HttpResponse ist, schreibe mir doch, dass ich dran denken soll, das noch zu ändern: website@nicostern.de - Hoffentlich sieht das niemals jemand")
        else:
            errors = form.errors
    else:
        form = RSVPform()
        errors = None
    return render(request, "wedsite/index.html", {
        "form": form,
        "errors": errors,
        "dropzone_url": os.getenv("DROPZONE_URL"),
        "qr_img": qr_img_base64,
    })

def antworten(request):
    guests_coming = RSVP.objects.filter(attending=True)
    guests_not_coming = RSVP.objects.filter(attending=False)
    
    sum_coming = 0
    sum_adults = 0
    for guest in guests_coming:
        sum_coming += 1 + (int)(guest.partner) + guest.kids
        sum_adults += 1 + (int)(guest.partner)
        
    sum_kids = sum(guest.kids for guest in guests_coming)
    
    for guest in guests_coming:
        guest.partner = "kommt" if guest.partner else "kommt nicht"        
    
    return render(request, "wedsite/antworten.html", {
        "guests_coming": guests_coming,
        "guests_not_coming": guests_not_coming,
        "sum_zusagen": len(guests_coming),
        "sum_coming": sum_coming,
        "sum_abgesagt": len(guests_not_coming),
        "sum": len(guests_coming) + len(guests_not_coming),
        "sum_kids": sum_kids,
        "sum_adults": sum_adults
    })