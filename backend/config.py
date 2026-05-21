from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '')
OPENAI_API_KEY    = os.getenv('OPENAI_API_KEY', '')

ETSY_CLIENT_ID     = os.getenv('ETSY_CLIENT_ID', '')
ETSY_CLIENT_SECRET = os.getenv('ETSY_CLIENT_SECRET', '')
ETSY_REDIRECT_URI  = os.getenv('ETSY_REDIRECT_URI', 'http://localhost:3456/etsy/callback')

PRINTIFY_API_KEY = os.getenv('PRINTIFY_API_KEY', '')

BACKEND_PORT = int(os.getenv('BACKEND_PORT', '8000'))

# Model tiers
MODEL_HAIKU  = 'claude-haiku-4-5-20251001'
MODEL_SONNET = 'claude-sonnet-4-6'
MODEL_OPUS   = 'claude-opus-4-7'
