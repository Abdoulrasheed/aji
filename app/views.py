from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.template.loader import get_template
import requests
import json
from datetime import timedelta, date, datetime
#from weasyprint import HTML, CSS

from key.aws_keys import APPSYNC_API_KEY, APPSYNC_API_ENDPOINT_URL
from functools import reduce
from .models import Gate

headers = {
    'Content-Type': "application/json",
    'x-api-key': APPSYNC_API_KEY,
    'cache-control': "no-cache",
}

@login_required
def home(request):
	context = {}
	template = 'app/home.html'
	return render(request, template, context)

def execute_gql(**kwargs):
	gate_no = kwargs.get('gate_number')
	date = kwargs.get('date')

	facility_no = kwargs.get('facility_number')

	gate_no = f'Gate {gate_no}'

	facility_no = f'Facility {facility_no}'

	query = '''
		query { 
			listJummApps(limit: 10000) 
					{ items {
						itemType fee date deviceName receiptType 
						} 
					} 
				}'''
					
	data = requests.request("POST", APPSYNC_API_ENDPOINT_URL, json={'query': query}, headers=headers)
	
	input_dict = data.json()['data']['listJummApps']

	# filter 'Gates Pass' data by gate number

	gate_output_dict = []
	for x in input_dict['items']:
		if x['deviceName'] == gate_no and x['receiptType'] == 'Gate Pass' and x['date'] == date:
			gate_output_dict.append(x)

	# filter 'Loading/Offloading' data by gate number

	loading_offloading_output_dict = []
	for x in input_dict['items']:
		if x['deviceName'] == gate_no and x['receiptType'] == 'Loading/Offloading' and x['date'] == date:
			loading_offloading_output_dict.append(x)

	# filter 'Facility' data by Facility number

	facility_output_dict = []
	for x in input_dict['items']:
		if x['deviceName'] == facility_no and x['date'] == date:
			facility_output_dict.append(x)
			
	data = [gate_output_dict, loading_offloading_output_dict, facility_output_dict]
	return data


@login_required
def get_data(request):
	gate_number = request.GET.get('gate_number')

	date = request.GET.get('date')

	q = execute_gql(gate_number=gate_number, date=date)

	if not q:
		return HttpResponse('NoData')

	overall_totals = []
	all_type_total_and_amount = []

	for n in range(0, len(q)):
		all_fees = [q[n][i]['fee'] for i in range(0, len(q[n]))]
		# get sum of fee

		if all_fees:
			total_amount = reduce(lambda x, y: (int(x) + int(y)), all_fees)
		else:
			total_amount = 0

		overall_totals.append(total_amount)

		values_ = {}
		amounts = {}
		for i in range(0, len(q[n])):
			amounts[f"{q[n][i]['itemType']}Amount"] = q[n][i]['fee']
			if q[n][i]['itemType'] not in values_:
				values_[q[n][i]['itemType']] = int(q[n][i]['fee'])
			else:
				values_[q[n][i]['itemType']] += int(q[n][i]['fee'])

		type_total_and_amount = [] # [['Cars', 28360, 40],  ['Cars', 28360, 40]]

		[[type_total_and_amount.append([v, values_[v], amounts[i]]),] for i, v in zip(amounts, values_)]

		all_type_total_and_amount.append(type_total_and_amount)
	temp = 'app/data.html'

	if gate_number in ('Facility 1', 'Facility 2'):
		temp = 'app/facility.html'

	q_data = render_to_string(temp, {
		'q':all_type_total_and_amount, 'gate_number': gate_number, 'total_amount': overall_totals})

	data = {
		'q': q_data,
		'total': total_amount
		}
	return HttpResponse(q_data)