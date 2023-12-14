from flask import Flask, render_template, request, redirect, url_for, flash, session , jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,IntegerField, DecimalField
from wtforms.validators import DataRequired, Length
from config import Config
import pandas as pd
import plotly.express as px
from datetime import datetime  # Import datetime module
import plotly.graph_objs as go
import plotly.offline as pyo
import plotly.io as pio
from forms import PeFundForm
from forms import IdeaForm
from forms import EditIdeaForm

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)






# Defind PE fund
class PeFund(db.Model):
    __tablename__ = 'funds'
    fundid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fundname = db.Column(db.String(255), nullable=False)
    vintageyear = db.Column(db.Integer)
    fundsize = db.Column(db.Numeric(18, 2))
    fundfocus = db.Column(db.String(100))
    geographicfocus = db.Column(db.String(100))
    generalpartner = db.Column(db.String(255))
    fundmanager = db.Column(db.String(255))
    fundadministrator = db.Column(db.String(255))
    fundlegalstructure = db.Column(db.String(50))
    funddomicile = db.Column(db.String(250))
    funddocuments = db.Column(db.Text)
    fundstatus = db.Column(db.String(20))
    fundstrategy = db.Column(db.Text)
    feestructure = db.Column(db.Text)
    regulatorycompliance = db.Column(db.String(255))
    auditfirm = db.Column(db.String(255))
    lastauditdate = db.Column(db.Date)
    investorrelationscontact = db.Column(db.String(255))
    expectedliquidationdate = db.Column(db.Date)

    def __init__(self, fundname, vintageyear, fundsize, fundfocus, geographicfocus, generalpartner, fundmanager,
                 fundadministrator, fundlegalstructure, funddomicile, funddocuments, fundstatus, fundstrategy,
                 feestructure, regulatorycompliance, auditfirm, lastauditdate, investorrelationscontact,
                 expectedliquidationdate):
        self.fundname = fundname
        self.vintageyear = vintageyear
        self.fundsize = fundsize
        self.fundfocus = fundfocus
        self.geographicfocus = geographicfocus
        self.generalpartner = generalpartner
        self.fundmanager = fundmanager
        self.fundadministrator = fundadministrator
        self.fundlegalstructure = fundlegalstructure
        self.funddomicile = funddomicile
        self.funddocuments = funddocuments
        self.fundstatus = fundstatus
        self.fundstrategy = fundstrategy
        self.feestructure = feestructure
        self.regulatorycompliance = regulatorycompliance
        self.auditfirm = auditfirm
        self.lastauditdate = lastauditdate
        self.investorrelationscontact = investorrelationscontact
        self.expectedliquidationdate = expectedliquidationdate

#define pe fund insert form
class FundForm(FlaskForm):
    fund_name = StringField('Fund Name')
    vintage_year = IntegerField('Vintage Year')
    fund_size = DecimalField('Fund Size')
    fund_focus = StringField('Fund Focus')
    # Add more fields for other fund details
    submit = SubmitField('Submit')


# Define the Fund model
class Fund(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    fund_description = db.Column(db.Text, nullable=True)
    fund_type = db.Column(db.String(50), nullable=True)
    benchmark = db.Column(db.String(100), nullable=True)


class FundReturn(db.Model):
    __tablename__ = 'fund_return'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    eom = db.Column(db.String(10))  # End of month date as string (e.g., '2023-07-31')
    return_percent = db.Column(db.Float)

    def __repr__(self):
        return f"<FundReturn {self.name} - {self.eom} - {self.return_percent}>"


class Idea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stock = db.Column(db.String(100), nullable=False)
    idea_type = db.Column(db.String(20), nullable=False)
    details = db.Column(db.Text, nullable=False)
    analyst = db.Column(db.String(20), nullable=False)
    insert_date = db.Column(db.DateTime, default=datetime.now)  # Add a date field with a default value
    
    def __init__(self, stock, idea_type, details,analyst,insert_date):
        self.stock = stock
        self.idea_type = idea_type
        self.details = details
        self.analyst = analyst
        self.insert_date = insert_date


# Fetch the fund details from the database
def fetch_fund_details_from_database():
    funds = Fund.query.all()
    return funds

@app.route('/fund_details')
def fund_details():
    # Fetch the fund details from the database and pass it to the template
    # You'll need to implement this part based on your database model and query.
    funds = fetch_fund_details_from_database()
    return render_template('fund_details.html', funds=funds)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            flash('Logged in successfully!', 'success')
            session['user'] = username
            return redirect(url_for('main_page'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html', form=form)


@app.route('/get_fund_returns')
def get_fund_returns():
    fund_name = request.args.get('fund_name')

    # Query the database to fetch fund return details based on the fund name
    fund_returns = FundReturn.query.filter_by(name=fund_name).all()



    # Convert the query results to a list of dictionaries
    fund_return_details = [{'eom': fr.eom, 'return_percent': fr.return_percent} for fr in fund_returns]

    # Return the fund return details as JSON
    return jsonify(fund_return_details)



# Function to get the fund return data from the database based on the fund name
def get_fund_return_data(fund_name):
    # Implement your code here to query the database and fetch the fund return data
    # For example, using SQLAlchemy to query the "FundReturn" model:
    fund_return_data = FundReturn.query.filter_by(name=fund_name).all()

    # Sort the data by date (eom)
    fund_return_data.sort(key=lambda x: x.eom)
    # Convert the data to a list of dictionaries for easier processing
    return [{'eom': item.eom, 'return_percent': item.return_percent} for item in fund_return_data]


# Implement the create_chart_figure function to create the chart figure
def create_chart_figure(x_values, y_values, fund_name):
    trace = go.Scatter(
        x=x_values,
        y=y_values,
        mode='lines',
        name='Fund Return',
    )

    layout = go.Layout(
        title=f'Fund Return Chart for {fund_name}',
        xaxis=dict(title='End of Month (EOM)'),
        yaxis=dict(title='Return Percentage'),
    )

    chart_data = [trace]
    chart = go.Figure(data=chart_data, layout=layout)
    return chart



# Implement the create_chart_html function to create the chart HTML
def create_chart_html(x_values, y_values):
    # Your implementation to create the chart HTML using Plotly goes here
    # For example, using Plotly Express:
    import plotly.express as px

    fig = px.line(x=x_values, y=y_values, title='Fund Return Chart')
    chart_html = fig.to_html()
    return chart_html



@app.route('/fund_chart/<fund_name>')
def get_fund_chart(fund_name):
    # Get the fund return data from the database based on the fund name
    fund_return_data = get_fund_return_data(fund_name)

    # Process the data to create the chart using Plotly
    x_values = [data['eom'].strftime('%Y-%m-%d') for data in fund_return_data]
    y_values = [data['return_percent'] for data in fund_return_data]

    # Create the chart figure
    chart = create_chart_figure(x_values, y_values, fund_name)

    # Return the JSON representation of the chart figure
    return chart.to_json()





# Route for the main page with the navigation bar
@app.route('/main_page')
def main_page():
    # Check if the user is logged in (you can use session data or any authentication method)
    # If the user is not logged in, redirect to the login page
    # Example using session:
    if 'user' not in session:
        return redirect('/login')

    return render_template('main_page.html')


# Route for the ideal sub-page
@app.route('/idea')
def idea():
    # Your ideal sub-page logic
    # Query the database to fetch the saved investment ideas
    ideas = Idea.query.all()
    
    # Render the "idea.html" template and pass the list of ideas to it
    return render_template('idea.html', ideas=ideas)
    
    
    #return render_template('ideal.html')

# Route for the stock research sub-page
@app.route('/stock_research')
def stock_research():
    # Your stock research sub-page logic
    return render_template('stock_research.html')

# Route for the portfolio sub-page
@app.route('/portfolio')
def portfolio():
    # Your portfolio sub-page logic
    return render_template('portfolio.html')


@app.route('/dashboard')
@login_required
def dashboard():
    return f'Hello, {current_user.username}! This is the dashboard.'


@app.route('/pe_funds')
@login_required
def pe_funds():
    # Fetch the PE fund data from the database
    funds = PeFund.query.all()
    return render_template('pe_funds.html', funds=funds)

@app.route('/submit_fund', methods=['GET', 'POST'])
def submit_fund():
    # Create an instance of your PeFundForm
    form = PeFundForm()

    if form.validate_on_submit():
        # Process the form data when it's submitted
        # You can access form fields like form.fundname.data, form.vintageyear.data, etc.
        # Perform database operations or other actions as needed
        
        # For example, to add a new fund to the database:
        new_fund = PeFund(
            fundname=form.fundname.data,
            vintageyear=form.vintageyear.data,
            fundsize=form.fundsize.data,
            fundfocus=form.fundfocus.data,
            geographicfocus=form.geographicfocus.data,
            generalpartner=form.generalpartner.data,
            fundmanager=form.fundmanager.data,
            fundadministrator=form.fundadministrator.data,
            fundlegalstructure=form.fundlegalstructure.data,
            funddomicile=form.funddomicile.data,
            funddocuments=form.funddocuments.data,
            fundstatus=form.fundstatus.data,
            fundstrategy=form.fundstrategy.data,
            feestructure=form.feestructure.data,
            regulatorycompliance=form.regulatorycompliance.data,
            auditfirm=form.auditfirm.data,
            lastauditdate=form.lastauditdate.data,
            investorrelationscontact=form.investorrelationscontact.data,
            expectedliquidationdate=form.expectedliquidationdate.data
            # Add other fields here
        )
        db.session.add(new_fund)
        db.session.commit()

        # Optionally, you can redirect to a success page or the pe_funds page
        flash('PE Fund submitted successfully!', 'success')
        return redirect(url_for('pe_funds'))

    # If the request method is GET, simply render the submit_fund.html template
    return render_template('submit_fund.html', form=form)



@app.route('/submit_idea', methods=['GET', 'POST'])
def submit_idea():
    # Create an instance of your PeFundForm
    form = IdeaForm()

    if form.validate_on_submit():
        # Process the form data when it's submitted
        # You can access form fields like form.fundname.data, form.vintageyear.data, etc.
        # Perform database operations or other actions as needed
        
        # For example, to add a new fund to the database:
        new_Idea = Idea(
		stock=form.stock.data, 
		idea_type=form.idea_type.data,
		details=form.details.data,
		analyst=form.analyst.data, 
		insert_date=form.insert_date.data,
            
        )
        db.session.add(new_Idea)
        db.session.commit()

        # Optionally, you can redirect to a success page or the pe_funds page
        flash('new_Idea submitted successfully!', 'success')
        return redirect(url_for('idea'))

    # If the request method is GET, simply render the submit_idea.html template
    return render_template('submit_idea.html', form=form)




# Set the default page to the login page
@app.route('/')
def default_page():
    return redirect('/login')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# In your Flask application (app.py)

@app.route('/save_idea', methods=['POST'])
def save_idea():
    if request.method == 'POST':
        # Extract data from the submitted form
        stock = request.form.get('stock')
        idea_type = request.form.get('idea_type')
        details = request.form.get('details')

        # Get the current date and time
        insert_date = datetime.now()

        # Get the username of the currently logged-in user
        analyst = current_user.username

        # Create a new Idea object and save it to the database
        new_idea = Idea(stock=stock, idea_type=idea_type, details=details, analyst=analyst, insert_date=insert_date )
        db.session.add(new_idea)
        db.session.commit()

        flash('Investment idea saved successfully!', 'success')
    
    # Redirect to the page where you display investment ideas (e.g., '/idea')
    return redirect(url_for('idea'))


@app.route('/delete_idea/<int:idea_id>', methods=['DELETE'])
def delete_idea(idea_id):
    # Find the idea by its idea_id and delete it from the database
    # Replace this with your database logic (using SQLAlchemy or your chosen library)
    idea = Idea.query.get(idea_id)
    if idea:
        db.session.delete(idea)
        db.session.commit()
        return jsonify(success='Idea deleted successfully')
    else:
        return jsonify(error='Idea not found'), 404

@app.route('/edit_idea/<int:idea_id>', methods=['GET'])
def edit_idea(idea_id):
    # Fetch the idea from the database based on idea_id
    idea = Idea.query.get(idea_id)

    if idea:
        form = EditIdeaForm(obj=idea)
        return render_template('edit_idea.html', form=form, idea_id=idea_id)
    else:
        flash('Idea not found', 'error')
        return redirect(url_for('idea'))


@app.route('/edit_idea/<int:idea_id>', methods=['POST'])
def update_idea(idea_id):
    # Fetch the idea from the database based on idea_id
    idea = Idea.query.get(idea_id)

    if idea:
        # Get form data
        stock  = request.form.get('stock')
        idea_type = request.form.get('idea_type')
        analyst = request.form.get('analyst')
        insert_date  = request.form.get('insert_date')
        details = request.form.get('details')
        
     
        # Update idea attributes
        idea.stock = stock
        idea.idea_type = idea_type
        idea.analyst = analyst
        idea.insert_date = insert_date
        idea.details = details


        # Commit changes to the database
        db.session.commit()

        flash('Idea updated successfully', 'success')
        return redirect(url_for('idea'))
    else:
        flash('Idea not found', 'error')
        return redirect(url_for('idea'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000,debug=True)