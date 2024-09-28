## app.py
from flask import Flask, render_template, redirect, url_for, flash, request
from config import Config
from models import db, Person, ItemSpec, Item
from forms import PersonForm, ItemSpecForm, DeliverForm, ReceiveForm, PersonSearchForm
import jdatetime

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return redirect(url_for('deliver'))

@app.route('/add_person', methods=['GET', 'POST'])
def add_person():
    form = PersonForm()
    if form.validate_on_submit():
        person = Person(
            full_name=form.full_name.data,
            unit=form.unit.data,
            phone=form.phone.data,
            description=form.description.data
        )
        db.session.add(person)
        db.session.commit()
        flash('شخص جدید ثبت شد', 'success')
        return redirect(url_for('add_person'))
    return render_template('add_person.html', form=form)

@app.route('/add_item_spec', methods=['GET', 'POST'])
def add_item_spec():
    form = ItemSpecForm()
    if form.validate_on_submit():
        item_spec = ItemSpec(
            item_name=form.item_name.data,
            asset_number=form.asset_number.data,
            description=form.description.data
        )
        db.session.add(item_spec)
        db.session.commit()
        flash('کالای جدید ثبت شد', 'success')
        return redirect(url_for('add_item_spec'))
    return render_template('add_item.html', form=form)

@app.route('/deliver', methods=['GET', 'POST'])
def deliver():
    form = DeliverForm()
    form.person_id.choices = [(p.id, p.full_name) for p in Person.query.all()]
    form.item_spec_id.choices = [(i.id, f"{i.item_name} - {i.asset_number}") for i in ItemSpec.query.all()]
    if form.validate_on_submit():
        now = jdatetime.datetime.now()
        date_out = now.strftime('%Y/%m/%d')
        time_out = now.strftime('%H:%M:%S')

        item = Item(
            person_id=form.person_id.data,
            item_spec_id=form.item_spec_id.data,
            deliverer=form.deliverer.data,
            quantity=form.quantity.data,
            date_out=date_out,
            time_out=time_out
        )
        db.session.add(item)
        db.session.commit()
        flash('تحویل کالا ثبت شد', 'success')
        return redirect(url_for('deliver'))
    return render_template('deliver.html', form=form)

@app.route('/receive', methods=['GET', 'POST'])
def receive():
    form = ReceiveForm()
    if form.validate_on_submit():
        item_spec = ItemSpec.query.filter_by(asset_number=form.asset_number.data).first()
        if item_spec:
            item = Item.query.filter_by(item_spec_id=item_spec.id, date_in=None).first()
            if item:
                now = jdatetime.datetime.now()
                date_in = now.strftime('%Y/%m/%d')
                time_in = now.strftime('%H:%M:%S')
                item.date_in = date_in
                item.time_in = time_in
                db.session.commit()
                flash('کالا به انبار برگشت داده شد', 'success')
                return redirect(url_for('receive'))
            else:
                flash('این کالا در حال حاضر خارج از انبار نیست یا قبلاً برگشت داده شده است', 'danger')
        else:
            flash('کالایی با این شماره اموال یافت نشد', 'danger')
    return render_template('receive.html', form=form)

@app.route('/report')
def report():
    items_out = Item.query.filter_by(date_in=None).all()
    return render_template('report.html', items_out=items_out)

@app.route('/print/<int:item_id>')
def print_item(item_id):
    item = Item.query.get_or_404(item_id)
    return render_template('print.html', item=item)

@app.route('/person_items', methods=['GET', 'POST'])
def person_items():
    form = PersonSearchForm()
    form.person_id.choices = [(p.id, p.full_name) for p in Person.query.all()]
    if form.validate_on_submit():
        person = Person.query.get(form.person_id.data)
        items = Item.query.filter_by(person_id=person.id, date_in=None).all()
        return render_template('person_items.html', person=person, items=items, form=form)
    return render_template('person_items.html', form=form, items=None)
    
if __name__ == '__main__':
    app.run(debug=True)
