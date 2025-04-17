import os
import json

CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'runtime_config.json')

DEFAULT_CONFIG = {
    'TWILIO_ACCOUNT_SID': os.getenv('TWILIO_ACCOUNT_SID', ''),
    'TWILIO_AUTH_TOKEN': os.getenv('TWILIO_AUTH_TOKEN', ''),
    'TWILIO_PHONE_NUMBER': os.getenv('TWILIO_PHONE_NUMBER', ''),
    'ELEVENLABS_API_KEY': os.getenv('ELEVENLABS_API_KEY', ''),
    'ELEVENLABS_AGENT_ID': os.getenv('ELEVENLABS_AGENT_ID', 'h3dC4sQ9cPDtYItAe0Z8'),
    'LLM_API_KEY': os.getenv('LLM_API_KEY', ''),
}

def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH) as f:
            return json.load(f)
    return DEFAULT_CONFIG.copy()

def save_config(new_config):
    with open(CONFIG_PATH, 'w') as f:
        json.dump(new_config, f)

def get_config():
    config = load_config()
    # fallback to env if missing
    for k, v in DEFAULT_CONFIG.items():
        if not config.get(k):
            config[k] = v
    return config
