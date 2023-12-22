from flask import Flask, render_template, request, url_for
import mysql.connector
import sys



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
    income_and_expenses_data = []

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
                
                
                cursor.execute(
                    """
                    UPDATE budget_app
                    SET total_expenses = (rent + groceries + entertainment + transport),
                    income_after_expenses = (monthly_income - total_expenses) WHERE id = 1
                    """
                    
                    )
                
                
                db.commit()
                
                cursor.execute("SELECT total_expenses, income_after_expenses FROM budget_app")
                table_row = cursor.fetchall()
                
                col_names = [name[0] for name in cursor.description]
                
                for row in table_row:
                    financial_details_dict = {}
                    for col_name, value in zip(col_names, row):
                        financial_details_dict[col_name] = value
                    income_and_expenses_data.append(financial_details_dict)  
                    
            else:
                print("hello")
                
        
    print(income_and_expenses_data, file=sys.stdout)
        
    return render_template("index.html", data = income_and_expenses_data)


    



if __name__ == "__main__":
    app.run(debug = True, use_reloader = False)
    
    
#cursor.execute("DELETE FROM budget_app")
#db.commit()
    

    
    
    
    
        
    #app.run(debug = True, use_reloader = False)