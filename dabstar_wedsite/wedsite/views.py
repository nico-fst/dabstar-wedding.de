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
        fields = ['name', 'email', 'attending', 'partner']

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
            raise forms.ValidationError("He, du hast ausgewählt, dass du 1 und 2 Kinder mitbringst: Bitte wähle nur eins aus.")
        cleaned_data["kids"] = 1 if child_1 else 2 if child_2 else 0

        # Guard: not coming, but bringing guests???
        attending = self.cleaned_data.get("attending")
        partner = self.cleaned_data.get("partner")
        if not attending and (cleaned_data["kids"] != 0 or partner):
            raise forms.ValidationError(
                "Öhm, du hast angegeben, dass du nicht kommst, aber Gäste mitbringst? Das passt nicht so ganz: Bitte korrigiere das."
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
            return HttpResponse("Danke für deine Anmeldung!")
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

def location(request):
    return render(request, "wedsite/location.html")
