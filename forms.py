from flask import Flask, render_template, request 
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField ,DateField,IntegerField
from wtforms import DecimalField, RadioField, SelectField, TextAreaField, FileField 
from wtforms.validators import InputRequired 
from datetime import date

class PeFundForm(FlaskForm): 
    fundname = StringField('Fund Name', validators=[InputRequired()])
    vintageyear = IntegerField('Vintage Year')
    fundsize = DecimalField('Fund Size', places=2)
    fundfocus = StringField('Fund Focus')
    geographicfocus = StringField('Geographic Focus')
    generalpartner = StringField('General Partner')
    fundmanager = StringField('Fund Manager')
    fundadministrator = StringField('Fund Administrator')
    fundlegalstructure = StringField('Fund Legal Structure')
    funddomicile = StringField('Fund Domicile')
    funddocuments = TextAreaField('Fund Documents')
    fundstatus = StringField('Fund Status')
    fundstrategy = TextAreaField('Fund Strategy')
    feestructure = TextAreaField('Fee Structure')
    regulatorycompliance = StringField('Regulatory Compliance')
    auditfirm = StringField('Audit Firm')
    lastauditdate = DateField('Last Audit Date')
    investorrelationscontact = StringField('Investor Relations Contact')
    expectedliquidationdate = DateField('Expected Liquidation Date')



class IdeaForm(FlaskForm): 
    stock = StringField('stock', validators=[InputRequired()])
    idea_type = SelectField('Idea type', choices=[
        ('Buy', 'Buy'),
        ('Sell', 'Sell'),
        ('Review', 'Review')
    ])


    details = TextAreaField('details')
    analyst = SelectField('Analyst', choices=[
        ('Leon', 'Leon'),
        ('Josephine', 'Josephine'),
        ('Mark', 'Mark')
    ])
    
    insert_date = DateField('Insert Date', default=date.today) 

class EditIdeaForm(FlaskForm):
    stock = StringField('Stock', validators=[InputRequired()])
    idea_type= SelectField('Idea type', choices=[
        ('Buy', 'Buy'),
        ('Sell', 'Sell'),
        ('Review', 'Review')
    ])
    details = TextAreaField('Details')
    analyst = SelectField('Analyst', choices=[
        ('Leon', 'Leon'),
        ('Josephine', 'Josephine'),
        ('Mark', 'Mark')
    ])
    insert_date = DateField('Insert Date')
