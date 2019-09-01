from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from .models import Vehicle
from django.db.models import Sum
from django.template.loader import render_to_string

import requests
import json

from key.aws_keys import APPSYNC_API_KEY, APPSYNC_API_ENDPOINT_URL
#url = 'https://api.graph.cool/simple/v1/ciyz901en4j590185wkmexyex'

headers = {
    'Content-Type': "application/json",
    'x-api-key': APPSYNC_API_KEY,
    'cache-control': "no-cache",
}

def execute_gql(query):
    payload_obj = {"query": query}
    payload = json.dumps(payload_obj)
    response = requests.request("POST", APPSYNC_API_ENDPOINT_URL, data=payload, headers=headers)
    return response

@login_required
def home(request):
	query = "query { listJummApis { items { vehicleType fees datetime gateNum username } } }"
	data = execute_gql(query)
	json_data = data.json()['data']['listJummApis']
	#d = json.loads(json_data)
	data = [i for i in json_data['items']]
	data = [data[i] for i in range(0, len(data))]
	context = {'data': data}
	template = 'app/table.html'
	return render(request, template, context)

@login_required
def load_graph_data(request):
	q = Vehicle.objects.all()

	total_amount = q.aggregate(
		total=Sum('amount')).get('total')

	v_types = []
	labels = [v_types.append(i.v_type) for i in q if i.v_type not in v_types]

	values_ = {}
	for i in q:
		if i.v_type not in values_:
			values_[i.v_type] = i.amount
		else:
			values_[i.v_type] += i.amount

	values = []
	for key, value in values_.items():
	    values.append(value)

	temp = 'async/v_type.html'
	print(values_)
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




def graph(request):
	pass
	