from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

# Vervang dit met je daadwerkelijke DATABASE_URL
DATABASE_URL = "postgresql://postgres.eupxuakhfykloqrojzbr:peZGTKWfDmLCcSWn@aws-0-eu-central-1.pooler.supabase.com:6543/postgres"

try:
    engine = create_engine(DATABASE_URL)
    connection = engine.connect()
    print("✅ Verbinding met de database is succesvol!")
    connection.close()
except OperationalError as e:
    print("❌ Database verbinding mislukt:")
    print(e)
