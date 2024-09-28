##forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError
from models import Person, ItemSpec

class PersonForm(FlaskForm):
    full_name = StringField('نام و نام خانوادگی', validators=[DataRequired()])
    unit = StringField('واحد')
    phone = StringField('تلفن')
    description = TextAreaField('توضیحات')
    submit = SubmitField('ثبت شخص')

    def validate_full_name(self, full_name):
        person = Person.query.filter_by(full_name=full_name.data).first()
        if person:
            raise ValidationError('این نام و نام خانوادگی قبلاً ثبت شده است.')

class ItemSpecForm(FlaskForm):
    item_name = StringField('نام کالا', validators=[DataRequired()])
    asset_number = StringField('شماره اموال', validators=[DataRequired()])
    description = TextAreaField('توضیحات')
    submit = SubmitField('ثبت کالا')

    def validate_asset_number(self, asset_number):
        item_spec = ItemSpec.query.filter_by(asset_number=asset_number.data).first()
        if item_spec:
            raise ValidationError('این شماره اموال قبلاً ثبت شده است.')

class DeliverForm(FlaskForm):
    person_id = SelectField('شخص تحویل گیرنده', coerce=int, validators=[DataRequired()])
    item_spec_id = SelectField('نام کالا', coerce=int, validators=[DataRequired()])
    deliverer = StringField('شخص تحویل دهنده', validators=[DataRequired()])
    quantity = IntegerField('تعداد', validators=[DataRequired()])
    submit = SubmitField('ثبت تحویل')

class ReceiveForm(FlaskForm):
    asset_number = StringField('شماره اموال', validators=[DataRequired()])
    submit = SubmitField('برگشت به انبار')

class PersonSearchForm(FlaskForm):
    person_id = SelectField('انتخاب شخص', coerce=int, validators=[DataRequired()])
    submit = SubmitField('جستجو')
