from flask import Flask, render_template, request, url_for,redirect
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
        savings_paid = request.form.get("savings_paid")
        debt_paid = request.form.get("debt_paid")
        

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
                    
        
    return render_template("index.html", data = income_and_expenses_data)


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
    return redirect(url_for('monthly_expenses'))


@app.route("/financial_progress", methods = ["GET", "POST"])
def display_progress():
    cursor.execute("SELECT debt, debt_paid, debt_to_pay, pct_debt_repaid, savings_target_year, savings_paid, pct_to_savings_goal FROM budget_app")
    financial_progress_rows = cursor.fetchall()
    
    col_names = [name[0] for name in cursor.description]    
    financial_progress_list = []
    
    for row in financial_progress_rows:
        financial_progress_dict = {}
        for col_name, value in zip(col_names, row):
            financial_progress_dict[col_name] = value
        financial_progress_list.append(financial_progress_dict)
        
    return render_template("financial_progress.html", financial_progress = financial_progress_list)


@app.route("/update_financial_information", methods = ["GET", "POST"])
def update_financial_information():
    
    financial_data_lst = []
    if request.method == "POST":
        monthly_income = request.form.get("monthly_income")
        rent = request.form.get("rent")
        groceries = request.form.get("groceries")
        entertainment = request.form.get("entertainment")
        transport = request.form.get("transport")
        
        cursor.execute(
            """
            UPDATE budget_app
            SET monthly_income = %s,
            rent = %s,
            groceries = %s,
            entertainment = %s,
            transport = %s
            WHERE id = 1
            """,
            (monthly_income, rent, groceries, entertainment, transport)
            )
        
        
        cursor.execute(
            """UPDATE budget_app
               SET total_expenses = (rent + groceries + entertainment + transport),
                income_after_expenses = (monthly_income - total_expenses) 
                WHERE id = 1
            
            """
            
            )
        
        db.commit()
        
        cursor.execute("SELECT total_expenses, income_after_expenses FROM budget_app")
        show_total_expense_and_income = cursor.fetchall()
        
        col_names = [name[0] for name in cursor.description]
        
        
        for row in show_total_expense_and_income:
            financial_data_dict = {}
            for col_name, value in zip(col_names, row):
                financial_data_dict[col_name] = value
            financial_data_lst.append(financial_data_dict)
    
    
    return render_template("update_information.html", financial_data = financial_data_lst)


        
#cursor.execute("DELETE FROM budget_app")
#db.commit()

if __name__ == "__main__":
    app.run(debug = True, use_reloader = False) 
    
    

    
    
    
    
    
        
    #app.run(debug = True, use_reloader = False)