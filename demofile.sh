
mkdir templates 
python3 scaffold.py user username password email phone country_id:references
python3 scaffold.py country name
python3 scaffold.py city country_id:references name
python3 scaffold.py logement titre description city_id:references
python3 scaffold.py userhasmusicalmood logement_id  musicalinstrument_id:references mood_musicale_id:references user_id
python3 scaffold.py logementhasphoto photo_id logement_id user_id
python3 scaffold.py poster_photo_numerique pic user_id iphone_css_overlay
python3 scaffold.py logementhasoutdoor outdoor_activity_id logement_id user_id
python3 scaffold.py musicalinstrument name
python3 scaffold.py outdoor_activity name
python3 scaffold.py mood_musicale name
python3 scaffold.py experience_decouverte_ia job_voyage_musique_description usurpation_ai_job_hacker_expliques
python3 scaffold.py spend_time_city experience_decouverte_ia_id:references outdoor_activity_id user_id test_identite_description
python3 scaffold.py photo pic:file description
