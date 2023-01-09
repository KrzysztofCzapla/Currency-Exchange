from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
# to get url api
import requests, json, os

def index(request):
	# API provides rates from a currency to PLN(Polish Zloty)

	# Try to get API from NBP
	# If not working raise error
	try:
		#get url
		body = requests.get("http://api.nbp.pl/api/exchangerates/tables/A/")

		# pack in json
		response = body.json()
	except:
		raise Http404("API can't be loaded")

	# Save API as variable
	currency_data = response[0]['rates']

	# set basic context
	context = {"currency_data":currency_data, "result": 0}

	if request.method == "POST":

		# Get Amount, if user click without posting data just set to 0 to avoid errors
		try:
			amount = float(request.POST.get("amount"))
		except:
			amount = 0
		
		# testing
		print(amount)

		# Get Currences codes from and to
		currency_from = request.POST.get("currency_from")
		currency_to = request.POST.get("currency_to")

		# if its not PLN
		if currency_from != "PLN":
			# Scan for wanted currency
			for c in currency_data:
				# if currency is found
				if c['code'] == currency_from:
					# get the amount in PLN
					amount *= float(c['mid'])

		# testing
		print(amount)

		for c in currency_data:
				if c['code'] == currency_to:
					# check how much is amount in other currency
					amount /= float(c['mid'])

		# shorten the result
		result = "{:.2f}".format(amount)

		#testing
		print(amount)

		# give variables to the templates
		context = {
		"result":result, 
		"currency_to":currency_to, 
		"currency_data":currency_data
		}

	return render(request, 'main/index.html', context)
	