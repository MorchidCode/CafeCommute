from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
from form import CafeForm


app = Flask(__name__)
app.config['SECRET_KEY'] = '7BYkEfBA6O6donzWlSihBXox7C0sKR2b'

Bootstrap5(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(app)

class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    city_area = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(200), nullable=False)
    sets = db.Column(db.Integer, nullable=False)
    wifi = db.Column(db.String(200), nullable=False)




with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template('index.html')

@app.route("/all-cafes")
def all_cafes():
    page = request.args.get('page', 1, type=int)
    per_page = 12  # Cafes per page
    cafes = Cafe.query.paginate(page=page, per_page=per_page)
    return render_template('all-cafes.html', cafes=cafes)

@app.route("/add-cafe", methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()

    if form.validate_on_submit():
        new_cafe = Cafe(
            name = form.name.data,
            city_area = form.city_area.data,
            url = form.google_maps_url.data,
            image = form.image_url.data,
            sets = form.num_of_seats.data,
            wifi = form.wifi_quality.data
        )

        db.session.add(new_cafe)
        db.session.commit()

        return redirect(url_for("home"))
    
    return render_template('add-cafe.html', form=form, title="Add cafe")

@app.route("/cafe/<int:id>", )
def cafe_detail(id):
    cafe = db.get_or_404(Cafe, id)
    return render_template('cafe-detail.html', cafe=cafe)

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_cafe(id):
    cafe = db.get_or_404(Cafe, id)
    
    form = CafeForm(
        name = cafe.name,
        city_area = cafe.city_area,
        image_url = cafe.image,
        google_maps_url = cafe.url,
        num_of_seats = cafe.sets,
        wifi_quality = cafe.wifi
    )

    form.submit.label.text = 'Update Cafe'

    if form.validate_on_submit():
        cafe.name = form.name.data
        cafe.city_area = form.city_area.data
        cafe.image = form.image_url.data
        cafe.url = form.google_maps_url.data
        cafe.sets = form.num_of_seats.data
        cafe.wifi = form.wifi_quality.data
        db.session.commit()
        return redirect(url_for('cafe_detail', id=cafe.id))
    
    return render_template('add-cafe.html', form=form)


@app.route("/delete/<int:id>")
def delete(id):
    cafe = db.get_or_404(Cafe, id)
    db.session.delete(cafe)
    db.session.commit()
    return redirect(url_for('all_cafes'))


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")