import sqlite3
from bottle import route, run, request, template

@route('/', method='GET')
def index():
    data = {'title': 'Welcome!'} 
    return template('welcome', data)   # show list of links


@route('/getDepartment', method = ['GET', 'POST'])
def department():
    if request.method == 'GET':
        return template('dept_form')
    else:
        dept = request.forms.get("dept")
        conn = sqlite3.connect("payroll.db")
        cur = conn.cursor()
        
        sql = '''SELECT pay_data.emp_id, emp_name, wage, hrs_worked FROM employees
                JOIN pay_data
                WHERE pay_data.emp_id = employees.emp_id AND employees.department = ?'''
        cur.execute(sql, (dept,))

        rows = cur.fetchall()
        cur.close()
        hrs = 0
        wage = 0

        if rows:

            dataList = []
            for row in rows:
                eid, name, wage, hrs = row
                if hrs <= 40:
                    payout = wage * hrs
                else:
                    ot_pay = (hrs - 40) * 1.5 * wage
                    payout = (wage * 40) + ot_pay

                emp = (eid, name, wage, hrs, payout)
                dataList.append(emp)

            data = {'rows': dataList, 'dept': dept}
            return template('show_department', data)

        else:
            msg = 'no such username'

            

@route('/editHours', method = ['GET', 'POST'])
def edit_hrs():
    if request.method == 'GET':
        return template('edit_hours')
    else:
        hrs_worked = request.forms.get('hrs')
        emp_id = request.forms.get('eid')
        
        conn = sqlite3.connect("payroll.db")
        cur = conn.cursor()

        try:
            sql = "UPDATE pay_data SET hrs_worked = ? WHERE emp_id = ?"
            cur.execute(sql, (hrs_worked, emp_id))
            conn.commit()
            m = {'msg' : 'insert successful'}

        except sqlite3.Error as er:
            m = {'msg' : 'insert unsuccessful'}
            

        finally:
            cur.close()

        return template('status', m)



run(host='localhost', port=8080) 
