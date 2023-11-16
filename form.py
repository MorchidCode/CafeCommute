from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, URL

class CafeForm(FlaskForm):
    name = StringField('Cafe Name', validators=[DataRequired()])
    city_area = StringField('City and Area', validators=[DataRequired()])
    image_url = StringField('Image URL', validators=[DataRequired(), URL()])
    google_maps_url = StringField('Google Maps URL', validators=[DataRequired(), URL()])
    num_of_seats = IntegerField('Number of Seats', validators=[DataRequired()])
    wifi_quality = SelectField('WiFi Quality', 
                               choices=[('⭐'), 
                                        ('⭐⭐'), 
                                        ('⭐⭐⭐'), 
                                        ('⭐⭐⭐⭐'), 
                                        ('⭐⭐⭐⭐⭐')],
                               validators=[DataRequired()])
    submit = SubmitField('Add Cafe')