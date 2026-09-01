from flask import Flask, render_template, request, session, redirect
from myplace import Myplace
from bs4 import BeautifulSoup
import subprocess
import os
from yourappdb import query_db, get_db
from flask import g

app = Flask(__name__)
app.secret_key="any string"
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
init_db()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def hello_world():
    user = query_db('select * from contacts')
    the_username = "anonyme"
    one_user = query_db('select * from contacts where first_name = ?',
                [the_username], one=True)
    return render_template("hey.html", users=user, one_user=one_user, the_title="my title")
@app.route("/add_one_user", methods=["GET","POST"])
def add_one_user():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslescountry= query_db("select * from country")

        one_user = query_db("insert into user (username,password,email,phone,country_id) values (:username,:password,:email,:phone,:country_id)",hey, one=True)
        mylastrowid=str(one_user["myid"])
        user = query_db('select * from user')


        last_user = query_db("select * from user where email = ? and password = ?",[hey["email"], hey["password"]], one=True)
        session["current_user_id"]=last_user["id"]
        for x in ['username','password','email','phone','country_id']:
            session[x]=hey[x]


        return render_template("userform.html", users=user, one_user=one_user, the_title="add new user", touslescountry=touslescountry)


    touslescountry= query_db("select * from country")

    user = query_db('select * from user')
    one_user = query_db("select * from user limit 1", one=True)
    return render_template("userform.html", users=user, one_user=one_user, the_title="add new user", touslescountry=touslescountry)


@app.route("/user_sign_out", methods=["GET","POST"])
def user_sign_out():
    if request.method == 'POST':
        session["current_user_id"]=""
        for x in ['username','password','email','phone','country_id']:
            session[x]=""
        return redirect("/")


@app.route("/user_log_in", methods=["GET","POST"])
def user_login():
    if request.method == 'POST':
        hey=request.form
        last_user = query_db("select * from user where email = ? and password = ?",[hey["email"], hey["password"]], one=True)
        try:
            session["current_user_id"]=last_user["id"]
            for x in ['username','password','email','phone','country_id']:
                session[x]=hey[x]
        except:
            return render_template("userlogin.html")
    return render_template("userlogin.html")
@app.route("/add_one_country", methods=["GET","POST"])
def add_one_country():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into country (name) values (:name)",hey, one=True)
        mylastrowid=str(one_user["myid"])
        user = query_db('select * from country')


        return render_template("countryform.html", countrys=user, one_user=one_user, the_title="add new country")


    user = query_db('select * from country')
    one_user = query_db("select * from country limit 1", one=True)
    return render_template("countryform.html", countrys=user, one_user=one_user, the_title="add new country")

@app.route("/add_one_city", methods=["GET","POST"])
def add_one_city():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslescountry= query_db("select * from country")

        one_user = query_db("insert into city (country_id,name) values (:country_id,:name)",hey, one=True)
        mylastrowid=str(one_user["myid"])
        user = query_db('select * from city')


        return render_template("cityform.html", citys=user, one_user=one_user, the_title="add new city", touslescountry=touslescountry)


    touslescountry= query_db("select * from country")

    user = query_db('select * from city')
    one_user = query_db("select * from city limit 1", one=True)
    return render_template("cityform.html", citys=user, one_user=one_user, the_title="add new city", touslescountry=touslescountry)

@app.route("/add_one_logement", methods=["GET","POST"])
def add_one_logement():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslescity= query_db("select * from city")

        one_user = query_db("insert into logement (titre,description,city_id) values (:titre,:description,:city_id)",hey, one=True)
        mylastrowid=str(one_user["myid"])
        user = query_db('select * from logement')


        return render_template("logementform.html", logements=user, one_user=one_user, the_title="add new logement", touslescity=touslescity)


    touslescity= query_db("select * from city")

    user = query_db('select * from logement')
    one_user = query_db("select * from logement limit 1", one=True)
    return render_template("logementform.html", logements=user, one_user=one_user, the_title="add new logement", touslescity=touslescity)

@app.route("/add_one_userhasmusicalmood", methods=["GET","POST"])
def add_one_userhasmusicalmood():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslesmusicalinstrument= query_db("select * from musicalinstrument")

        touslesmood_musicale= query_db("select * from mood_musicale")

        one_user = query_db("insert into userhasmusicalmood (logement_id,musicalinstrument_id,mood_musicale_id,user_id) values (:logement_id,:musicalinstrument_id,:mood_musicale_id,:user_id)",hey, one=True)
        mylastrowid=str(one_user["myid"])
        user = query_db('select * from userhasmusicalmood')


        return render_template("userhasmusicalmoodform.html", userhasmusicalmoods=user, one_user=one_user, the_title="add new userhasmusicalmood", touslesmusicalinstrument=touslesmusicalinstrument, touslesmood_musicale=touslesmood_musicale)


    touslesmusicalinstrument= query_db("select * from musicalinstrument")

    touslesmood_musicale= query_db("select * from mood_musicale")

    user = query_db('select * from userhasmusicalmood')
    one_user = query_db("select * from userhasmusicalmood limit 1", one=True)
    return render_template("userhasmusicalmoodform.html", userhasmusicalmoods=user, one_user=one_user, the_title="add new userhasmusicalmood", touslesmusicalinstrument=touslesmusicalinstrument, touslesmood_musicale=touslesmood_musicale)

@app.route("/add_one_logementhasphoto", methods=["GET","POST"])
def add_one_logementhasphoto():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into logementhasphoto (photo_id,logement_id,user_id) values (:photo_id,:logement_id,:user_id)",hey, one=True)
        mylastrowid=str(one_user["myid"])
        user = query_db('select * from logementhasphoto')


        return render_template("logementhasphotoform.html", logementhasphotos=user, one_user=one_user, the_title="add new logementhasphoto")


    user = query_db('select * from logementhasphoto')
    one_user = query_db("select * from logementhasphoto limit 1", one=True)
    return render_template("logementhasphotoform.html", logementhasphotos=user, one_user=one_user, the_title="add new logementhasphoto")

@app.route("/add_one_poster_photo_numerique", methods=["GET","POST"])
def add_one_poster_photo_numerique():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into poster_photo_numerique (pic,user_id,iphone_css_overlay) values (:pic,:user_id,:iphone_css_overlay)",hey, one=True)
        mylastrowid=str(one_user["myid"])
        user = query_db('select * from poster_photo_numerique')


        return render_template("poster_photo_numeriqueform.html", poster_photo_numeriques=user, one_user=one_user, the_title="add new poster_photo_numerique")


    user = query_db('select * from poster_photo_numerique')
    one_user = query_db("select * from poster_photo_numerique limit 1", one=True)
    return render_template("poster_photo_numeriqueform.html", poster_photo_numeriques=user, one_user=one_user, the_title="add new poster_photo_numerique")

@app.route("/add_one_logementhasoutdoor", methods=["GET","POST"])
def add_one_logementhasoutdoor():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into logementhasoutdoor (outdoor_activity_id,logement_id,user_id) values (:outdoor_activity_id,:logement_id,:user_id)",hey, one=True)
        mylastrowid=str(one_user["myid"])
        user = query_db('select * from logementhasoutdoor')


        return render_template("logementhasoutdoorform.html", logementhasoutdoors=user, one_user=one_user, the_title="add new logementhasoutdoor")


    user = query_db('select * from logementhasoutdoor')
    one_user = query_db("select * from logementhasoutdoor limit 1", one=True)
    return render_template("logementhasoutdoorform.html", logementhasoutdoors=user, one_user=one_user, the_title="add new logementhasoutdoor")

@app.route("/add_one_musicalinstrument", methods=["GET","POST"])
def add_one_musicalinstrument():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into musicalinstrument (name) values (:name)",hey, one=True)
        mylastrowid=str(one_user["myid"])
        user = query_db('select * from musicalinstrument')


        return render_template("musicalinstrumentform.html", musicalinstruments=user, one_user=one_user, the_title="add new musicalinstrument")


    user = query_db('select * from musicalinstrument')
    one_user = query_db("select * from musicalinstrument limit 1", one=True)
    return render_template("musicalinstrumentform.html", musicalinstruments=user, one_user=one_user, the_title="add new musicalinstrument")

@app.route("/add_one_outdoor_activity", methods=["GET","POST"])
def add_one_outdoor_activity():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into outdoor_activity (name) values (:name)",hey, one=True)
        mylastrowid=str(one_user["myid"])
        user = query_db('select * from outdoor_activity')


        return render_template("outdoor_activityform.html", outdoor_activitys=user, one_user=one_user, the_title="add new outdoor_activity")


    user = query_db('select * from outdoor_activity')
    one_user = query_db("select * from outdoor_activity limit 1", one=True)
    return render_template("outdoor_activityform.html", outdoor_activitys=user, one_user=one_user, the_title="add new outdoor_activity")

@app.route("/add_one_mood_musicale", methods=["GET","POST"])
def add_one_mood_musicale():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into mood_musicale (name) values (:name)",hey, one=True)
        mylastrowid=str(one_user["myid"])
        user = query_db('select * from mood_musicale')


        return render_template("mood_musicaleform.html", mood_musicales=user, one_user=one_user, the_title="add new mood_musicale")


    user = query_db('select * from mood_musicale')
    one_user = query_db("select * from mood_musicale limit 1", one=True)
    return render_template("mood_musicaleform.html", mood_musicales=user, one_user=one_user, the_title="add new mood_musicale")

@app.route("/add_one_experience_decouverte_ia", methods=["GET","POST"])
def add_one_experience_decouverte_ia():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into experience_decouverte_ia (job_voyage_musique_description,usurpation_ai_job_hacker_expliques) values (:job_voyage_musique_description,:usurpation_ai_job_hacker_expliques)",hey, one=True)
        mylastrowid=str(one_user["myid"])
        user = query_db('select * from experience_decouverte_ia')


        return render_template("experience_decouverte_iaform.html", experience_decouverte_ias=user, one_user=one_user, the_title="add new experience_decouverte_ia")


    user = query_db('select * from experience_decouverte_ia')
    one_user = query_db("select * from experience_decouverte_ia limit 1", one=True)
    return render_template("experience_decouverte_iaform.html", experience_decouverte_ias=user, one_user=one_user, the_title="add new experience_decouverte_ia")

@app.route("/add_one_spend_time_city", methods=["GET","POST"])
def add_one_spend_time_city():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslesexperience_decouverte_ia= query_db("select * from experience_decouverte_ia")

        one_user = query_db("insert into spend_time_city (experience_decouverte_ia_id,outdoor_activity_id,user_id,test_identite_description) values (:experience_decouverte_ia_id,:outdoor_activity_id,:user_id,:test_identite_description)",hey, one=True)
        mylastrowid=str(one_user["myid"])
        user = query_db('select * from spend_time_city')


        return render_template("spend_time_cityform.html", spend_time_citys=user, one_user=one_user, the_title="add new spend_time_city", touslesexperience_decouverte_ia=touslesexperience_decouverte_ia)


    touslesexperience_decouverte_ia= query_db("select * from experience_decouverte_ia")

    user = query_db('select * from spend_time_city')
    one_user = query_db("select * from spend_time_city limit 1", one=True)
    return render_template("spend_time_cityform.html", spend_time_citys=user, one_user=one_user, the_title="add new spend_time_city", touslesexperience_decouverte_ia=touslesexperience_decouverte_ia)

@app.route("/add_one_photo", methods=["GET","POST"])
def add_one_photo():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)

        uploaded_file = request.files['pic']
        if uploaded_file.filename != '':
            uploaded_file.save(os.path.join('static/photos', uploaded_file.filename))

        hey["pic"]=uploaded_file.filename


        one_user = query_db("insert into photo (pic,description) values (:pic,:description)",hey, one=True)
        mylastrowid=str(one_user["myid"])
        user = query_db('select * from photo')


        return render_template("photoform.html", photos=user, one_user=one_user, the_title="add new photo")


    user = query_db('select * from photo')
    one_user = query_db("select * from photo limit 1", one=True)
    return render_template("photoform.html", photos=user, one_user=one_user, the_title="add new photo")

