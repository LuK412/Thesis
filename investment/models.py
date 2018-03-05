from otree.api import (
	models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
	Currency as c, currency_range
)

import random

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
	name_in_url = 'investment'
	players_per_group = None
	num_rounds = 1

	endowment_principals = c(10)

	# Fixed Compensation
	fixed_payment = c(10)

	#Variable Compensation
	variable_payment = c(5)			# Fixer Anteil für die Agenten
	share = 25

class Subsession(BaseSubsession):
	
	def creating_session(self):					
		for player in self.get_players():
			player.treatment = self.session.config["treatment"]
			player.compensation = self.session.config["compensation"]
			player.participation_fee = self.session.config['participation_fee']


class Group(BaseGroup):
	pass


class Player(BasePlayer):

# Roles:
	# gerade Nummern sind Kunden
	def role(self):
		if self.id_in_group % 2 == 0:
			return "Customer"
		else:
			return "Agent"


	

# Part II Choosing Category:
	
	category = models.CharField(
		choices=["Sehr konservativ", "Sicherheitsorientiert", "Ausgeglichen", "Wachstumsorientiert", "Offensiv"],
		widget=widgets.RadioSelect(),
		verbose_name="Bitte wählen Sie nun einen der fünf Begriffe:",
		doc="Principals choose the category which is communicated to their agent"
		)

	category_received = models.CharField(
		doc="Category that agents see (from their customers)."
		)


# Part II Investment:

	investment_single = models.CurrencyField(
		min=0,
		max=Constants.endowment_principals,
		widget=widgets.Slider(),					# Neuer Slider von Christian
		verbose_name="Ihre Investitionsentscheidung für Ihren Kunden:",
		doc="Agents investment for the principal in the risky asset."
		)

	invested_amount = models.CurrencyField(
		doc="What was invested by the corresponding agent."
		)

	investment_outcome = models.CharField()
	investment_outcome_agents = models.CharField()

	payoff = models.CurrencyField()
	payoff_customer = models.CurrencyField(
		doc="Payoff of the agent's principal."
		)



	def risky_asset(self):
		self.random_number=random.randint(1,3)

		if self.id_in_group % 2 == 0:
			if self.random_number == 1:
				self.investment_outcome="Die Investition war erfolgreich."
			else:
				self.investment_outcome="Die Investition war nicht erfolgreich."


	def payments_agents(self):
		if self.id_in_group % 2 != 0: # Für Agenten
			if self.session.config["compensation"] == "fixed":
				self.payoff=Constants.fixed_payment
			if self.session.config["compensation"] == "variable":
				self.payoff=Constants.variable_payment   + Constants.share/100 * self.payoff_customer

	def payments_customers(self):
		if self.id_in_group % 2 == 0:
			if self.investment_outcome == "Die Investition war erfolgreich.":
				self.payoff=self.invested_amount * 3.5 + (Constants.endowment_principals - self.invested_amount)
			elif self.investment_outcome == "Die Investition war nicht erfolgreich.":
				self.payoff=Constants.endowment_principals - self.invested_amount




# Results: Messages

	message = models.CharField(
		choices=["Ich bin sehr zufrieden mit Ihrer Entscheidung", "Ich bin zufrieden mit Ihrer Entscheidung",
		"Ich bin unzufrieden mit Ihrer Entscheidung", "Ich bin sehr unzufrieden mit Ihrer Entscheidung"],
		widget=widgets.RadioSelect(),
		verbose_name="Wählen Sie dazu eine der vorgefertigten Mitteilungen aus:",
		doc="Principals choose the message to send to the agents."
		)

	message_received = models.CharField(
		doc="Message that agents receive from their principals."
		)
	




# 

	treatment = models.CharField(
		doc="Treatment (either single or group)"
		)

	compensation = models.CharField(
		doc="Compensation scheme put in place for agents (see settings)."
		)

	participation_fee = models.CharField(
		doc="Participation Fee for all agents."
		)




# Questionnaire:

	age = models.PositiveIntegerField(
		max=100,
		verbose_name="Wie alt sind Sie?",
		doc="We ask participants for their age between 0 and 100 years"
		)

	gender = models.CharField(
		choices=["männlich", "weiblich", "anderes"],
		widget=widgets.RadioSelect(),
		verbose_name="Was ist Ihr Geschlecht?",
		doc="gender indication"
		)

	studies = models.CharField(
		blank=True,
		verbose_name="Was studieren Sie im Hauptfach?",
		doc="field of studies indication."
		)

	studies2 = models.BooleanField(
		widget=widgets.CheckboxInput(),
		verbose_name="Kein Student",
		doc="Ticking the checkbox means that the participant is a non-student.")

	financial_advice = models.CharField(
		choices=["Ja", "Nein"],
		widget=widgets.RadioSelect(),
		verbose_name="Haben Sie bereits eine Bankberatung in Anspruch genommen?",
		doc="We ask participants if they ever made use of financial advice.")

	income = models.CurrencyField(
		verbose_name="Wie viel Geld im Monat steht Ihnen frei zur Verfügung?",
		doc="We ask participants how much money they have freely available each month.")
