from flask import Flask, render_template, request, redirect, url_for
import yaml
import os

app = Flask(__name__)
CONFIG_FILE_PATH = os.path.join('..', 'config', 'config.yaml') # Percorso relativo al file config.yaml

def load_config():
    """Carica la configurazione dal file YAML."""
    try:
        with open(CONFIG_FILE_PATH, 'r') as file:
            config = yaml.safe_load(file) or {} # Se file vuoto, carica un dizionario vuoto
        return config
    except FileNotFoundError:
        return {} # Se file non trovato, restituisce un dizionario vuoto

def save_config(config_data):
    """Salva la configurazione nel file YAML."""
    with open(CONFIG_FILE_PATH, 'w') as file:
        yaml.dump(config_data, file, indent=2)

@app.route('/', methods=['GET', 'POST'])
def config_page():
    config = load_config()
    instagram_config = config.get('instagram', {}) # Prende la config instagram esistente o un dizionario vuoto

    if request.method == 'POST':
        instagram_config['app_id'] = request.form.get('instagram_app_id')
        instagram_config['app_secret'] = request.form.get('instagram_app_secret')
        instagram_config['page_access_token'] = request.form.get('instagram_page_access_token')
        instagram_config['instagram_business_account_id'] = request.form.get('instagram_business_account_id')

        config['instagram'] = instagram_config # Aggiorna la sezione instagram nella config principale
        save_config(config)
        return redirect(url_for('config_page')) # Ricarica la pagina per mostrare i valori salvati

    return render_template('config.html', instagram_config=instagram_config)

if __name__ == '__main__':
    app.run(debug=True) # debug=True SOLO per sviluppo, disabilitare in produzione
