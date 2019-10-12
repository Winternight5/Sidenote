from flask_table import Table, Col
 
class Results(Table):
    id = Col('Id', show=False)
    username = Col('username')
    email = Col('email')