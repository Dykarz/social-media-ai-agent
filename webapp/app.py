from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages, jsonify
import yaml
import os
from integrations.instagram.instagram_api import test_instagram_connection as instagram_test_conn
from integrations.twitter.twitter_api import test_twitter_connection as twitter_test_conn

app = Flask(__name__)
app.secret_key = "super segreto"
CONFIG_FILE_PATH = os.path.join('..', 'config', 'config.yaml')

def load_config():
    """Carica la configurazione dal file YAML."""
    try:
        with open(CONFIG_FILE_PATH, 'r') as file:
            config = yaml.safe_load(file) or {}
        return config
    except FileNotFoundError:
        return {}

def save_config(config_data):
    """Salva la configurazione nel file YAML."""
    with open(CONFIG_FILE_PATH, 'w') as file:
        yaml.dump(config_data, file, indent=2)

@app.route('/', methods=['GET', 'POST']) # Route per Configurazione (pagina principale)
def config_page():
    config = load_config()
    instagram_config = config.get('instagram', {})
    twitter_config = config.get('twitter', {})

    if request.method == 'POST':
        form_type = request.form.get('form_type')

        if form_type == 'instagram':
            instagram_config['app_id'] = request.form.get('instagram_app_id')
            instagram_config['app_secret'] = request.form.get('instagram_app_secret')
            instagram_config['page_access_token'] = request.form.get('instagram_page_access_token')
            instagram_config['instagram_business_account_id'] = request.form.get('instagram_business_account_id')
            config['instagram'] = instagram_config
            flash('Configurazione Instagram salvata con successo!', 'success')

        elif form_type == 'twitter':
            twitter_config['twitter_api_key'] = request.form.get('twitter_api_key')
            twitter_config['twitter_api_secret_key'] = request.form.get('twitter_api_secret_key')
            twitter_config['twitter_access_token'] = request.form.get('twitter_access_token')
            twitter_config['twitter_access_token_secret'] = request.form.get('twitter_access_token_secret')
            config['twitter'] = twitter_config
            flash('Configurazione Twitter salvata con successo!', 'success')
        
        save_config(config)
        return redirect(url_for('config_page'))

    return render_template('config.html', instagram_config=instagram_config, twitter_config=twitter_config, messages=get_flashed_messages(with_categories=True))


@app.route('/profiles') # NUOVA ROUTE per Profili Social
def profiles_page():
    """Route per la pagina dei Profili Social (per ora dati SIMULATI)."""
    # Dati profilo Instagram SIMULATI (da sostituire con dati veri API in futuro)
    instagram_profile_data = {
        'username': 'instagram_username_simulato',
        'biography': 'Biografia di test di Instagram',
        'followers_count': 1234,
        'following_count': 567,
        'profile_picture_url': 'URL_IMMAGINE_PROFILO_INSTAGRAM_SIMULATO' # Potremmo usare URL immagine placeholder
    }
    # Dati profilo Twitter SIMULATI (da sostituire con dati veri API in futuro)
    twitter_profile_data = {
        'username': 'TwitterUsernameSimulato',
        'name': 'Nome Utente Twitter Simulato',
        'bio': 'Bio di test di Twitter',
        'followers_count': 987,
        'following_count': 654,
        'profile_picture_url': 'URL_IMMAGINE_PROFILO_TWITTER_SIMULATO' # Potremmo usare URL immagine placeholder
    }

    return render_template('config.html', # Rende lo stesso template config.html
                           show_profiles_section=True, # Passa flag per mostrare sezione profili
                           instagram_profile=instagram_profile_data, # Passa dati profilo Instagram
                           twitter_profile=twitter_profile_data) # Passa dati profilo Twitter


@app.route('/test_instagram_connection', methods=['POST'])
def test_instagram_connection_route():
    config_data = request.get_json()
    success, result = instagram_test_conn(config_data)
    if success:
        return jsonify({'success': True, 'username': result.get('username'), 'biography': result.get('biography'), 'followers_count': result.get('followers_count'), 'follows_count': result.get('follows_count')}), 200
    else:
        return jsonify({'success': False, 'error': result}), 400


@app.route('/test_twitter_connection', methods=['POST'])
def test_twitter_connection_route():
    config_data = request.get_json()
    success, result_message = twitter_test_conn(config_data)
    if success:
        return jsonify({'success': True, 'username': result_message}), 200
    else:
        return jsonify({'success': False, 'error': result_message}), 400


if __name__ == '__main__':
    app.run(debug=True)