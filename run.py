from market import app
from market import db

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables
        print("Database tables created.")
    app.run(debug=True)

