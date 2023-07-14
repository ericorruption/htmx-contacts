from flask import Blueprint, request

from models.contact import Contact

api_v1 = Blueprint('api_v1', __name__)


@api_v1.get('/contacts')
def json_contacts():
    contacts_list = Contact.all()
    contacts_dicts = [c.__dict__ for c in contacts_list]
    return {"contacts": contacts_dicts}


@api_v1.post('/contacts')
def json_contacts_create():
    c = Contact(None, request.form.get('name'), request.form.get('phone'),
                request.form.get('email'))
    if c.save():
        return c.__dict__
    else:
        return {"errors": c.errors}, 400


# TODO handle not found
@api_v1.get("/contacts/<contact_id>")
def json_contacts_view(contact_id=0):
    contact = Contact.find(contact_id)
    return contact.__dict__


@api_v1.put("/contacts/<contact_id>")
def json_contacts_edit(contact_id):
    c = Contact.find(contact_id)
    c.update(request.form['name'], request.form['phone'],
             request.form['email'])
    if c.save():
        return c.__dict__
    else:
        return {"errors": c.errors}, 400


@api_v1.delete("/contacts/<contact_id>")
def json_contacts_delete(contact_id=0):
    contact = Contact.find(contact_id)
    contact.delete()
    return jsonify({"success": True})
