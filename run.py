from app import create_app

# Maak de app aan
app = create_app()

if __name__ == '__main__':
    # Start de server
    app.run(debug=True)

