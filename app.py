# TODO autopep8
import os

from flask import Flask, redirect, request, render_template, flash

from models.contact import Contact  # TODO learn what WSGI is

app = Flask(__name__)

# Needed for e.g. flash messages
app.secret_key = os.getenv('SECRET_KEY')

Contact.load_db()


@app.get('/')
def index():
    return redirect("/contacts")


@app.get('/contacts')
def contacts():
    search = request.args.get('q')

    if search is not None:
        contacts_list = Contact.search(search)
    else:
        contacts_list = Contact.all()
    return render_template('contacts/index.html', contacts=contacts_list)


@app.post('/contacts')
def contacts_create():
    contact = Contact(
        name=request.form['name'], email=request.form['email'], phone=request.form['phone'])
    if contact.save():
        flash('Contact created successfully.')
        return redirect('/contacts')
    else:
        return render_template('contacts/new.html', contact=contact)


@app.get('/contacts/new')
def contacts_new():
    return render_template('contacts/new.html', contact=Contact())


@app.get('/contacts/<int:id>')
def contacts_show(id: int = 0):
    contact = Contact.find(id)
    return render_template('contacts/view.html', contact=contact)


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
