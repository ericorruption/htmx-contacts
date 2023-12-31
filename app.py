# TODO autopep8
import os

from flask import Flask, redirect, request, render_template, flash, send_file

from models.contact import Contact  # TODO learn what WSGI is
from lib.archiver import Archiver
from api.v1 import api_v1

Contact.load_db()

app = Flask(__name__)
app.register_blueprint(api_v1, url_prefix='/api/v1')

# Needed for e.g. flash messages
app.secret_key = os.getenv('SECRET_KEY')


@app.get('/')
def index():
    return redirect("/contacts")


@app.get('/contacts')
def contacts():
    search = request.args.get('q')
    page = int(request.args.get('page', 1))

    if search is not None:
        contacts_list = Contact.search(search)
        if request.headers.get('HX-Trigger') == 'search':
            return render_template('contacts/_list.html', contacts=contacts_list)
    else:
        contacts_list = Contact.all(page)
    return render_template('contacts/index.html', contacts=contacts_list, page=page, archiver=Archiver.get())


@app.post('/contacts')
def contacts_create():
    contact = Contact(
        name=request.form['name'], email=request.form['email'], phone=request.form['phone'])
    if contact.save():
        flash('Contact created successfully.')
        return redirect('/contacts')
    else:
        return render_template('contacts/new.html', contact=contact)


@app.post('/contacts/delete')
@app.delete('/contacts')
def contacts_delete_all():
    contact_ids = list(map(int, request.form.getlist("contact-ids[]")))
    for id in contact_ids:
        contact = Contact.find(id)
        contact.delete()
    flash('Contacts deleted successfully.')
    return redirect('/contacts', code=303)


@app.get('/contacts/count')
def contacts_count():
    return "(" + str(Contact.count()) + " total contacts)"


@app.get('/contacts/archive')
def contacts_archive():
    return render_template('archive.html', archiver=Archiver.get())


@app.post('/contacts/archive')
def create_contacts_archive():
    archiver = Archiver.get()
    archiver.run()
    return render_template('archive.html', archiver=archiver)


@app.delete('/contacts/archive')
def delete_contacts_archive():
    archiver = Archiver.get()
    archiver.reset()
    return render_template('archive.html', archiver=archiver)


@app.get('/contacts/archive/file')
def download_contacts_archive():
    archiver = Archiver.get()
    return send_file(archiver.archive_file(), 'archive.json', as_attachment=True)


@app.get('/contacts/new')
def contacts_new():
    return render_template('contacts/new.html', contact=Contact())


@app.get('/contacts/<int:id>')
def contacts_show(id: int = 0):
    contact = Contact.find(id)
    return render_template('contacts/view.html', contact=contact)


@app.get('/contacts/<int:id>/email')
def contacts_email(id: int = 0):
    contact = Contact.find(id)
    contact.email = request.args.get('email')
    contact.validate()
    return contact.errors.get('email') or ''


@app.get('/contacts/<int:id>/edit')
def contacts_edit(id: int = 0):
    contact = Contact.find(id)
    return render_template('contacts/edit.html', contact=contact)

# TODO refactor to use put


@app.post('/contacts/<int:id>/edit')
def contacts_update(id: int = 0):
    contact = Contact.find(id)
    contact.update(request.form['name'],
                   request.form['phone'], request.form['email'])
    if contact.save():
        flash('Contact updated successfully.')
        return redirect('/contacts/' + str(contact.id))
    else:
        return render_template('contacts/edit.html', contact=contact)


@app.delete('/contacts/<int:id>')
@app.post('/contacts/<int:id>/delete')
def contacts_delete(id: int = 0):
    contact = Contact.find(id)
    contact.delete()
    flash('Contact deleted successfully.')
    return redirect('/contacts', code=303)
