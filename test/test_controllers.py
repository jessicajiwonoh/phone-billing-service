import pytest
import json
from datetime import datetime, timedelta

from app import create_app

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        'TESTING':True,
    })
    
    yield app
    
@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

def test_call_request(client):
    response = client.get('/call/')
    response_data = json.loads(response.data)[0]

    assert response.status_code == 200
    assert 'id' in response_data
    assert 'customer_id' in response_data
    assert 'start_timestamp' in response_data
    assert 'end_timestamp' in response_data

def test_call_customer_request(client):
    response = client.get('/call/customer', data={
        'customer':2,
    })
    response_data =  json.loads(response.data)[0]

    assert response.status_code == 200
    assert response_data['customer_id'] == 2
    
def test_add_call(client):
    response = client.post('/call/add_call', data={
        'customer':2,
        'minutes':'20',
    })
    # New data added will be 2nd call for customer 2
    response_data =  json.loads(response.data)[1]

    start_time = response_data['start_timestamp']
    dt_start = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S.%f')
    end_time = response_data['end_timestamp']
    dt_end = datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S.%f')
    diff = dt_end - dt_start

    assert response.status_code == 200
    assert response_data['customer_id'] == 2
    assert diff == timedelta(minutes=20)

def test_invoice_request(client):
    response = client.get('/invoice/')
    response_data = json.loads(response.data)[0]

    assert response.status_code == 200
    assert 'id' in response_data
    assert 'customer_id' in response_data
    assert 'amount_billed' in response_data
    assert 'date_billed' in response_data
    assert 'date_paid' in response_data

def test_invoice_customer_request(client):
    response = client.get('/invoice/customer', data={
        'customer':1,
    })
    # Test data uses month 10
    response_data = json.loads(response.data)['10'][0][0]

    assert response.status_code == 200
    assert 'datetime' in response_data
    assert 'duration' in response_data
    assert 'rate' in response_data
    
def test_invoice_consolidated_request(client):
    response = client.get('/invoice/consolidated', data={
        'customer':1,
    })
    # Test data uses month 9
    response_data = json.loads(response.data)['9']

    assert response.status_code == 200
    assert response_data == 0.3

def test_invoice_month_request(client):
    response = client.get('/invoice/month', data={
        'customer':1,
        'month': 8
    })
    # Test data uses month 8
    response_data = json.loads(response.data)['8']

    assert response.status_code == 200
    assert response_data == 0.6

def test_generate_invoice(client):
    response = client.post('/invoice/generate_invoice', data={
        'customer':1,
    })

    if 'Today is not the first day of the month':
        assert response.status_code == 302
    else:
        assert response.status_code == 200
