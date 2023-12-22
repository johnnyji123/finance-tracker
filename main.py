from flask import Flask, render_template, request, url_for
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
def monthly_expenses():
    
    if request.method == "POST":
        cursor.execute("SELECT COUNT(*) FROM budget_app")
        monthly_income = request.form.get("monthly_income")
        rent = request.form.get("rent")
        groceries = request.form.get("groceries")
        entertainment = request.form.get("entertainment")
        transport = request.form.get("transport")
        debt = request.form.get("debt")
        savings_target = request.form.get("savings_target_year")
        
        for data in cursor:
            if data[0] == 0:
                cursor.execute(
                    """
                    INSERT INTO budget_app
                    (monthly_income,
                     rent,
                     groceries,
                     entertainment,
                     transport,
                     debt,
                     savings_target_year)
                    
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """
                    ,(monthly_income, rent, groceries, entertainment, transport, debt, savings_target)
                    )
                
                db.commit()
                    
            else:
                print("not empty")
                
        
        
    return render_template("index.html")
        
    



if __name__ == "__main__":
    app.run(debug = True, use_reloader = False)