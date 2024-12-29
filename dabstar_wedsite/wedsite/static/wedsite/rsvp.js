// RSVP: widersprüchliche Optionen deaktivieren

const fieldAttending = document.getElementById("id_attending");
const fieldNotAttending = document.getElementById("id_not_attending");
const fieldPartner = document.getElementById("id_partner");
const fieldChild1 = document.getElementById("id_child_1");
const fieldChild2 = document.getElementById("id_child_2");

const fieldsToDisable = [fieldPartner, fieldChild1, fieldChild2];
const labelsToDisable = fieldsToDisable.map((field) =>
  document.querySelector(`label[for=${field.id}]`)
);

// Hilfsfunktion: Felder und Labels aktivieren/deaktivieren
function toggleFields(disable, fields, labels) {
  fields.forEach((field) => {
    field.disabled = disable;
    if (disable) field.checked = false;
  });
  labels.forEach((label) => label.classList.toggle("disabled", disable));
}

// Event Listener für "Ich werde kommen"
fieldAttending.addEventListener("change", function () {
  if (fieldAttending.checked) {
    fieldNotAttending.checked = false;
    fieldNotAttending.disabled = true;
    toggleFields(false, fieldsToDisable, labelsToDisable); // Reaktiviert andere Felder
  } else {
    fieldNotAttending.disabled = false;
  }
});

// Event Listener für "Ich werde nicht kommen"
fieldNotAttending.addEventListener("change", function () {
  if (fieldNotAttending.checked) {
    fieldAttending.checked = false;
    fieldAttending.disabled = true;
    toggleFields(true, fieldsToDisable, labelsToDisable); // Deaktiviert andere Felder
  } else {
    fieldAttending.disabled = false;
  }
});
