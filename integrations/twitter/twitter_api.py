import tweepy
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

def test_twitter_connection(config_data): # Prende config_data come argomento
    """Testa la connessione all'API di Twitter e recupera username utente."""
    if not config_data or 'api_key' not in config_data or 'api_secret_key' not in config_data or 'access_token' not in config_data or 'access_token_secret' not in config_data:
        return False, "Configurazione Twitter incompleta" # Restituisce False e messaggio errore

    try:
        client = tweepy.Client(
            consumer_key=config_data['api_key'],
            consumer_secret=config_data['api_secret_key'],
            access_token=config_data['access_token'],
            access_token_secret=config_data['access_token_secret']
        )
        user = client.get_me() # Ottiene info utente
        if user and user.data and user.data.username:
            return True, user.data.username # Restituisce True e username
        else:
            return False, "Impossibile recuperare username utente Twitter." # Restituisce False e messaggio errore
    except tweepy.errors.TweepyException as e:
        return False, f"Errore di autenticazione Twitter API: {e}" # Restituisce False e messaggio errore


if __name__ == "__main__":
    # Esempio di test locale (rimosso per ora per evitare confusione, ma puoi riaggiungerlo se vuoi testare manualmente)
    pass