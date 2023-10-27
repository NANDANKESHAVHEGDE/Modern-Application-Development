from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, DecimalField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange

class AddProductForm(FlaskForm):
    product_id = StringField('Product ID', validators=[DataRequired(), Length(max=50)])
    category_id = StringField('Category ID', validators=[DataRequired(), Length(max=50)])
    category_name = StringField('Category Name', validators=[DataRequired(), Length(max=100)])
    product_name = StringField('Product Name', validators=[DataRequired(), Length(max=100)])
    manufacture_date = DateField('Manufacture Date', validators=[DataRequired()])
    expiry_date = DateField('Expiry Date', validators=[DataRequired()])
    price_per_unit = DecimalField('Price per Unit', validators=[DataRequired(), NumberRange(min=0)])
    stocks = IntegerField('Stocks', validators=[DataRequired(), NumberRange(min=0)])
    unit = StringField('Unit', validators=[DataRequired(), Length(max=50)])

class EditProductForm(FlaskForm):
    product_id = StringField('Product ID', validators=[DataRequired(), Length(max=50)])
    category_id = StringField('Category ID', validators=[DataRequired(), Length(max=50)])
    category_name = StringField('Category Name', validators=[DataRequired(), Length(max=100)])
    product_name = StringField('Product Name', validators=[DataRequired(), Length(max=100)])
    manufacture_date = DateField('Manufacture Date', validators=[DataRequired()])
    expiry_date = DateField('Expiry Date', validators=[DataRequired()])
    price_per_unit = DecimalField('Price per Unit', validators=[DataRequired(), NumberRange(min=0)])
    stocks = IntegerField('Stocks', validators=[DataRequired(), NumberRange(min=0)])
    unit = StringField('Unit', validators=[DataRequired(), Length(max=50)])
