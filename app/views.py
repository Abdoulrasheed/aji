from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.template.loader import get_template
import requests
import json
from datetime import timedelta, date, datetime
from weasyprint import HTML, CSS

from key.aws_keys import APPSYNC_API_KEY, APPSYNC_API_ENDPOINT_URL
from functools import reduce

headers = {
    'Content-Type': "application/json",
    'x-api-key': APPSYNC_API_KEY,
    'cache-control': "no-cache",
}

def execute_gql(**kwargs):
	if kwargs:
		from_ = kwargs['start']
		to = kwargs['end']
		if '/' in from_ or '/' in to:	
			# change dates to desired format: 2019-09-05
			from_ = datetime.strptime(from_, '%m/%d/%Y').strftime('%Y-%m-%d')
			to = datetime.strptime(to, '%m/%d/%Y').strftime('%Y-%m-%d')
	else:
		from_ = f'{date.today() - timedelta(days=1)}' # default to todays data
		to = f'{date.today()}'
	print(f'============================{from_}')

	query = '''
		query { 
			listJummApis(limit: 10000, filter:
				{ datetime: 
					{ between: ["%s", "%s"]}}) 
					{ items {
						vehicleType fees datetime gateNum username 
						} 
					} 
				}'''%(from_, to)

	payload_obj = {"query": query}
	payload = json.dumps(payload_obj)
	data = requests.request("POST", APPSYNC_API_ENDPOINT_URL, data=payload, headers=headers)
	json_data = data.json()['data']['listJummApis']

	data = [i for i in json_data['items']]
	data = [data[i] for i in range(0, len(data))]
	return data


def get_table_graph_data(**kwargs):
	if kwargs:
		start = kwargs['start']
		end = kwargs['end']

	# if the user tries to filter
	# then start and end will be available
	if all((start, end)):
		q = execute_gql(start=start, end=end)
	else:
		q = execute_gql() # query today's default data

	if not q:
		return HttpResponse('NoData')

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
	amounts = {}
	for i in range(0, len(q)):
		amounts[f"{q[i]['vehicleType']}Amount"] = q[i]['fees']
		if q[i]['vehicleType'] not in values_:
			values_[q[i]['vehicleType']] = q[i]['fees']
		else:
			values_[q[i]['vehicleType']] += q[i]['fees']

	type_total_and_amount = []
	'''
		eg [['Cars', 28360, 40],  ['Cars', 28360, 40]]
	'''
	[[type_total_and_amount.append([v, values_[v], amounts[i]]),] for i, v in zip(amounts, values_)]

	# get the actual non-repeatable fees in a list
	values = []
	for key, value in values_.items():
	    values.append(value)

	temp = 'async/v_type.html'

	q_data = render_to_string(temp, {'q':type_total_and_amount})

	data = {
		'values': values,
		'labels': v_types,
		'q': q_data,
		'total': total_amount
		}
	return data


@login_required
def load_graph_data(request):
	"""
		A view that fetches data from AWS graphQL AppSync
		Server and then loads the data in a html canvas of chart.js
	"""
	start = request.GET.get('start')
	end = request.GET.get('end')
	data = get_table_graph_data(start=start, end=end)

	return JsonResponse({"data": data})

@login_required
def home(request):
	"""
		the home page view that returns all data from api
	"""
	start = request.GET.get('start')
	end = request.GET.get('end')

	# if the user tries to filter
	# then 'start' and 'end' will both be true
	# therefore respond with a HttpResponse 
	# for ajax to consume the results
	if all((start, end)):
		data = execute_gql(start=start, end=end)
		if not data:
			return HttpResponse('NoData')
		template = 'async/ajax_table.html'
		data = render_to_string(template, {'data': data})
		return HttpResponse(data)
	else:
		data = execute_gql() # query today's default data

	context = {'data': data}
	template = 'app/table.html'
	return render(request, template, context)

@login_required
def statistics(request):
	context = {}
	template = 'app/stats.html'
	return render(request, template, context)

@login_required
def generate_report(request):
	start = request.GET.get('start')
	end = request.GET.get('end')
	print(start)
	print(end)

	if all((start, end)):
		template = 'reports/statistics_report.html'
		data = get_table_graph_data(start=start, end=end)
		print(f'data =================================\n{data}')

		context = {
			'data':data,
			'start': start,
			'end': end
		}

		template = get_template(template)
		html = template.render(context)

		css_string = """@page {
			size: a4 portrait;
			margin: 1mm;
			counter-increment: page;
		}"""

		pdf_file = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(
				stylesheets=[CSS(string=css_string)], presentational_hints=True)
		response = HttpResponse(pdf_file, content_type='application/pdf')
		response['Content-Disposition'] = 'filename="Report.pdf"'
		return response
		return HttpResponse(response.getvalue(), content_type='application/pdf')
	else:
		return HttpResponse('Please choose a date range')