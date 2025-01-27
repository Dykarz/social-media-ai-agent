from flask import Flask, render_template, request, redirect, url_for, flash
import yaml
import os

app = Flask(__name__)
app.secret_key = "super segreto" # Chiave segreta per usare Flask flash (messaggi di feedback)
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

@app.route('/', methods=['GET', 'POST'])
def config_page():
    config = load_config()
    instagram_config = config.get('instagram', {})
    twitter_config = config.get('twitter', {}) # Carica anche config Twitter

    if request.method == 'POST':
        form_type = request.form.get('form_type') # Determina quale form è stato inviato

        if form_type == 'instagram':
            instagram_config['app_id'] = request.form.get('instagram_app_id')
            instagram_config['app_secret'] = request.form.get('instagram_app_secret')
            instagram_config['page_access_token'] = request.form.get('instagram_page_access_token')
            instagram_config['instagram_business_account_id'] = request.form.get('instagram_business_account_id')
            config['instagram'] = instagram_config
            flash('Configurazione Instagram salvata con successo!', 'success') # Messaggio di successo

        elif form_type == 'twitter':
            twitter_config['twitter_api_key'] = request.form.get('twitter_api_key')
            twitter_config['twitter_api_secret_key'] = request.form.get('twitter_api_secret_key')
            twitter_config['twitter_access_token'] = request.form.get('twitter_access_token')
            twitter_config['twitter_access_token_secret'] = request.form.get('twitter_access_token_secret')
            config['twitter'] = twitter_config
            flash('Configurazione Twitter salvata con successo!', 'success') # Messaggio di successo
        
        save_config(config)
        return redirect(url_for('config_page')) # Ricarica per mostrare messaggi e valori salvati

    # Passa sia instagram_config che twitter_config al template
    return render_template('config.html', instagram_config=instagram_config, twitter_config=twitter_config, messages=flash_messages())

def flash_messages():
    """Recupera e formatta i messaggi flash di Flask per passarli al template."""
    messages = flash()
    formatted_messages = []
    for message, category in messages:
        formatted_messages.append({'message': message, 'category': category})
    return formatted_messages


if __name__ == '__main__':
    app.run(debug=True)