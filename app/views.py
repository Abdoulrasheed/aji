from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.db.models import Sum
from django.template.loader import render_to_string

import requests
import json

from key.aws_keys import APPSYNC_API_KEY, APPSYNC_API_ENDPOINT_URL
from functools import reduce

headers = {
    'Content-Type': "application/json",
    'x-api-key': APPSYNC_API_KEY,
    'cache-control': "no-cache",
}


@login_required
def execute_gql():
	query = "query { listJummApis { items { vehicleType fees datetime gateNum username } } }"
	payload_obj = {"query": query}
	payload = json.dumps(payload_obj)
	data = requests.request("POST", APPSYNC_API_ENDPOINT_URL, data=payload, headers=headers)
	json_data = data.json()['data']['listJummApis']
	#d = json.loads(json_data)
	data = [i for i in json_data['items']]
	data = [data[i] for i in range(0, len(data))]
	return data

@login_required
def home(request):
	data = execute_gql()
	context = {'data': data}
	template = 'app/table.html'
	return render(request, template, context)

@login_required
def load_graph_data(request):
	"""
		A view that gets data from AWS graphQL AppSync
		Server and then loads the data in a chart 

	"""

	# execute the API call
	q = execute_gql()

	all_fees = [q[i]['fees'] for i in range(0, len(q))]

	# get sum of all revenue paid (i.e fees)
	total_amount = reduce(lambda x, y: (x + y), all_fees)
	
	# get all vehicle labels for use in graph
	# making sure each label e.g: car appears only once
	# in the list: eg ['Cars', 'Cars', 'Cars', 'Napep']
	v_types = []
	[v_types.append(q[i]['vehicleType']) for i in range(0, len(q)) if q[i]['vehicleType'] not in v_types]

	# if same type of vehicle appears more than once
	# return the sum of fees of all of them
	# i.e to avoid having two instances of same type of vehicle type
	values_ = {}
	for i in range(0, len(q)):
		if q[i]['vehicleType'] not in values_:
			values_[q[i]['vehicleType']] = q[i]['fees']
		else:
			values_[q[i]['vehicleType']] += q[i]['fees']

	# get the actual the non-repeatable fees in a list
	values = []
	for key, value in values_.items():
	    values.append(value)

	temp = 'async/v_type.html'

	q_data = render_to_string(temp, {'q':values_})

	data = {
		'values': values,
		'labels': v_types,
		'q': q_data, 
		'total': total_amount
		}
	return JsonResponse(data)


@login_required
def start(request):
	context = {}
	template = 'app/stats.html'
	return render(request, template, context)