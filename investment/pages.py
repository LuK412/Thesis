from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Introduction(Page):
	pass


class Part_1(Page):
	pass


class Part_2_Instructions(Page):
	pass


class Customer(Page):
	
	form_model = "player"
	form_fields = ["category"]

	def before_next_page(self):		
		players = self.group.get_players()
		categories = [p.category for p in players]
		for p in players:
			if p.id_in_group < len(self.subsession.get_players()):
				p.category_received = categories[p.id_in_group]
			else:
				p.category_received = categories[0]


class WaitPage_1(WaitPage):

	def after_all_players_arrive(self):
		pass


class Agent_Single(Page):

	def is_displayed(self):
		return self.session.config["treatment"] == "single"
	
	form_model = "player"
	form_fields = ["investment_single"]

class WaitPage_2(WaitPage):

	def after_all_players_arrive(self):
		pass


class Versuch_2(Page):

	def before_next_page(self):	
		self.player.risky_asset()
		players = self.group.get_players()
		investments = [p.investment_single for p in players]
		investment_outcomes = [p.investment_outcome for p in players]
		for p in players:
			if p.id_in_group > 1 and p.id_in_group < len(self.subsession.get_players()):
				p.invested_amount = investments[p.id_in_group-2]
				p.investment_outcome_agents = investment_outcomes[p.id_in_group]
			elif p.id_in_group > 1 and p.id_in_group == len(self.subsession.get_players()):
				p.invested_amount = investments[p.id_in_group-2]
				p.investment_outcome_agents = investment_outcomes[0]
			elif p.id_in_group == 1 and p.id_in_group < len(self.subsession.get_players()):
				p.invested_amount = investments[-1]
				p.investment_outcome_agents = investment_outcomes[p.id_in_group]
			elif p.id_in_group == 1 and p.id_in_group == len(self.subsession.get_players()):
				p.invested_amount = investments[-1]
				p.investment_outcome_agents = investment_outcomes[0]
		self.player.payments_customers()


class Agent_Group(Page):

	def is_displayed(self):
		return self.session.config["treatment"] == "group"


class WaitPage_3(WaitPage):

	def after_all_players_arrive(self):
		pass

class Versuch(Page):

	def before_next_page(self):
		players = self.group.get_players()
		payoffs_customers = [p.payoff for p in players]
		for p in players:
			if p.id_in_group % 2 != 0 and p.id_in_group < len(self.subsession.get_players()):
				p.payoff_customer = payoffs_customers[p.id_in_group]
			if p.id_in_group % 2 != 0 and p.id_in_group == len(self.subsession.get_players()):
				p.payoff_customer = payoffs_customers[0]
		self.player.payments_agents()



class Results_Single_Customer(Page):

	def is_displayed(self):
		return self.session.config["treatment"] == "single" and self.player.role() == "Customer"
	
	form_model = "player"
	form_fields = ["message"]

	def before_next_page(self):		
		players = self.group.get_players()
		messages = [p.message for p in players]
		for p in players:
			if p.id_in_group < len(self.subsession.get_players()):
				p.message_received = messages[p.id_in_group]
			else:
				p.message_received = messages[0]


class WaitPage_4(WaitPage):
	pass

class Results_Single_Agent(Page):

	def is_displayed(self):
		return self.session.config["treatment"] == "single" and self.player.role() == "Agent"


class Results_Group(Page):

	def is_displayed(self):
		return self.session.config["treatment"] == "group"
	
	form_model = "player"
	form_fields = ["message"]


class Questionnaire(Page):

	form_model = "player"
	form_fields = ["age", "gender", "studies", "studies2", "financial_advice", "income"]


class Last_Page(Page):
	pass


page_sequence = [
#	Introduction,
#	Part_1,
#	Part_2_Instructions,
	Customer,
	WaitPage_1,
	Agent_Single,
	WaitPage_2,
	Versuch_2,
	Agent_Group,
	WaitPage_3,
	Versuch,
	Results_Single_Customer,
	WaitPage_4,
	Results_Single_Agent,
	Results_Group,
	Questionnaire,
	Last_Page
]
