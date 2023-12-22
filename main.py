from flask import Flask, render_template, request
import mysql.connector




db = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "projects123123",
        database = "finance_tracker"
    )


cursor = db.cursor()    

# table budget_app


app = Flask(__name__)

@app.route("/", methods = ["Post", "GET"])
def montly_expenses():
    
    return render_template("index.html")


    
if __name__ == "__main__":
    app.run(debug = True, use_reloader = False)