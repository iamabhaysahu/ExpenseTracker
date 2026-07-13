from Expensetracker import create_app,db

tracker =  create_app()

with tracker.app_context():
    db.create_all()

if __name__ == "__main__":
    tracker.run(debug=True)
    