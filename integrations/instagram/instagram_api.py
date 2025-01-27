import requests
import yaml

def load_config(config_file_path="config/config.yaml"):
    """Carica la configurazione da un file YAML."""
    try:
        with open(config_file_path, 'r') as file:
            config = yaml.safe_load(file) or {}
        return config
    except FileNotFoundError:
        print(f"Errore: File di configurazione non trovato: {config_file_path}")
        return None

def test_instagram_connection(config_data): # Prende config_data come argomento
    """Testa la connessione all'API di Instagram e recupera informazioni di base."""
    if not config_data or 'app_id' not in config_data or 'app_secret' not in config_data or 'page_access_token' not in config_data:
        return False, "Configurazione Instagram incompleta" # Restituisce False e messaggio di errore

    access_token = config_data['page_access_token']
    user_id = config_data.get('instagram_business_account_id') # Opzionale

    if not user_id:
        user_id_endpoint = 'https://graph.facebook.com/me/accounts'
        params = {
            'access_token': access_token
        }
        response = requests.get(user_id_endpoint, params=params)
        if response.status_code == 200:
            data = response.json()
            if data['data']:
                user_id = data['data'][0]['id'] # Prende il primo account collegato (pagina FB)
                print(f"Recuperato Instagram Business Account ID: {user_id}")
            else:
                return False, "Nessun account Instagram Business collegato alla Pagina Facebook." # Restituisce False e messaggio
        else:
            return False, f"Errore nel recupero dell'Instagram Business Account ID: {response.status_code} - {response.text}" # Restituisce False e messaggio

    if not user_id:
        return False, "Impossibile ottenere l'Instagram Business Account ID." # Restituisce False e messaggio

    profile_endpoint = f'https://graph.instagram.com/v17.0/{user_id}' # Versione API
    fields = 'username,biography,followers_count,follows_count,profile_picture_url'
    params = {
        'fields': fields,
        'access_token': access_token
    }

    try:
        response = requests.get(profile_endpoint, params=params)
        response.raise_for_status()
        profile_data = response.json()
        profile_info = { # Restituisce un dizionario con info profilo
            'username': profile_data.get('username', 'N/A'),
            'biography': profile_data.get('biography', 'N/A'),
            'followers_count': profile_data.get('followers_count', 'N/A'),
            'follows_count': profile_data.get('follows_count', 'N/A')
        }
        return True, profile_info # Restituisce True e info profilo

    except requests.exceptions.RequestException as e:
        error_message = f"Errore durante la connessione all'API di Instagram: {e}"
        if response is not None:
            error_message += f"\nStatus Code: {response.status_code}\nResponse Text: {response.text}"
        return False, error_message # Restituisce False e messaggio di errore

if __name__ == "__main__":
    # Esempio di test locale (rimosso per ora per evitare confusione, ma puoi riaggiungerlo se vuoi testare manualmente)
    pass