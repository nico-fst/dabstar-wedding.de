from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from .models import RSVP


class RSVPform(forms.ModelForm):
    class Meta:
        model = RSVP
        fields = "__all__"

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

    # Gäste-Feld
    guests = forms.IntegerField(
        widget=forms.NumberInput(  # Statt IntegerInput verwenden wir NumberInput
            attrs={"placeholder": "0-4"}
        ),
        label="Anzahl der Gäste",  # Optional: Label für Gäste
    )

    # Message-Feld (Optional)
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={"placeholder": "Optional - falls ihr uns noch etwas mitgeben möchtet :)"}
        ),
        required=False,  # Optionales Feld
        label=False
    )
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if RSVP.objects.filter(email=email).exists():
            raise forms.ValidationError("Hoppla, diese Email-Adresse wurde bereits registriert. Warst das nicht du? Wende dich gerne an website@nicostern.de :)")
        return email
    
    def clean(self):
        # Guard: not coming, but bringing guests???
        attending = self.cleaned_data.get('attending')
        guests = self.cleaned_data.get('guests')
        if not attending and not guests == 0:
            raise forms.ValidationError("Öhm, du hast angegeben, dass du nicht kommst, aber Gäste mitbringst? Das passt nicht so ganz. Bitte korrigiere das.")
        
    # def guard_

def index(request):
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
        "errors": errors
    })
