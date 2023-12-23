from flask import Flask, render_template, request, url_for,redirect
import mysql.connector
import sys



db = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "password",
        database = "finance_tracker"
    )


cursor = db.cursor()    

# table budget_app


app = Flask(__name__)

def fetchall_rows(query):
    cursor.execute(query)
    all_rows = cursor.fetchall()
    
    col_names = [name[0] for name in cursor.description]
    data_lst = []
    
    
    for row in all_rows:
        row_dict = {}
        for col_name, value in zip(col_names, row):
            row_dict[col_name] = value
        data_lst.append(row_dict)
       
    return data_lst
    


@app.route("/update_financial_information", methods = ["GET", "POST"])
def update_financial_information():
    
    financial_data_lst = []
    if request.method == "POST":
        monthly_income = request.form.get("monthly_income")
        rent = request.form.get("rent")
        groceries = request.form.get("groceries")
        entertainment = request.form.get("entertainment")
        transport = request.form.get("transport")
        debt = request.form.get("debt")
        savings_target = request.form.get("savings_target_year")
        
        cursor.execute(
            """
            UPDATE budget_app
            SET monthly_income = %s,
            rent = %s,
            groceries = %s,
            entertainment = %s,
            transport = %s,
            debt = %s,
            savings_target_year = %s
            WHERE id = 1
            """,
            (monthly_income, rent, groceries, entertainment, transport, debt, savings_target)
            )
        
        
        cursor.execute(
            """UPDATE budget_app
               SET total_expenses = (rent + groceries + entertainment + transport),
                income_after_expenses = (monthly_income - total_expenses) 
                WHERE id = 1
            
            """
            
            )
            
        db.commit()
        
        query = cursor.execute("SELECT total_expenses, income_after_expenses FROM budget_app")
        financial_data_lst = fetchall_rows(query)
        

    
    
    return render_template("update_information.html", financial_data = financial_data_lst)


@app.route("/savings_and_debt_repayment", methods = ["GET", "POST"])
def savings_and_debt_repayment():
    if request.method == "POST":
        savings_paid = request.form.get("savings_paid")
        debt_paid = request.form.get("debt_paid")
        
        cursor.execute("""
                       UPDATE budget_app SET debt_paid = %s, savings_paid = %s,
                       debt_to_pay = (debt - debt_paid),
                       pct_debt_repaid = ROUND((debt_paid / debt) * 100, 2),
                       pct_to_savings_goal = ROUND((savings_paid / savings_target_year) * 100, 2)
                       
                       WHERE id = 1""",
                       (debt_paid, savings_paid))
        
        
        db.commit()
        
    return redirect(url_for('update_financial_information'))


@app.route("/financial_progress", methods = ["GET", "POST"])
def display_progress():
    query = cursor.execute("SELECT debt, debt_paid, debt_to_pay, pct_debt_repaid, savings_target_year, savings_paid, pct_to_savings_goal FROM budget_app")
    financial_progress_lst = fetchall_rows(query)
    
     
    return render_template("financial_progress.html", financial_progress = financial_progress_lst)






if __name__ == "__main__":
    app.run(debug = True, use_reloader = False) 
    
    

    
    
    
    
        
