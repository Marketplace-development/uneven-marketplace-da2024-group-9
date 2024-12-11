print("config.py is geladen")
from supabase import create_client, Client

# Supabase configuratie
SUPABASE_URL = "https://aws-0-eu-central-1.pooler.supabase.com"
SUPABASE_KEY = "postgres.qnuzlfxmugobmzrehbwa:Bfg6WSGodQHfazaF"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
print("Supabase-client is aangemaakt")

