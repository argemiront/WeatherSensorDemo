import http.client
import json
import boto3
import datetime
from decimal import Decimal
import keys

def lambda_handler(event, context):
    '''
    This function will be triggered every time a modification is made on the database.
    If the modification is an INSERT, the function will add the first measure 
    and some other data related to the location.
    '''

    dynamodb = boto3.resource('dynamodb')
    tableMeasures = dynamodb.Table('sensors-hist')
    tableSensor = dynamodb.Table('sensors-data')
 
    base = keys.BASE
    key = keys.KEY
    units = keys.UNITS
    
    apiConn = http.client.HTTPConnection(base)
    
    for record in event['Records']:
        
        if record['eventName'] == 'INSERT':
            lat = record['dynamodb']['NewImage']['SensorLatitude']['N']
            lng = record['dynamodb']['NewImage']['SensorLongitude']['N']
            url = '/data/2.5/weather?lat=' + lat + '&lon=' + lng + units + key
            apiConn.request('GET', url)
            r1 = apiConn.getresponse()
            results = json.loads(r1.read())
            
            tableMeasures.put_item(
                Item={
                    'id': str(record['dynamodb']['NewImage']['id']['S'] + datetime.datetime.now().strftime("%Y-%m-%d&%H:%M:%S")),
                    'SensorID': record['dynamodb']['NewImage']['id']['S'],
                    'Date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'Temperature': Decimal(str(results['main']['temp'])),
                    'Humidity': Decimal(str(results['main']['humidity']))
                }
            )
            
            tableSensor.update_item(
                Key={
                    'id': record['dynamodb']['NewImage']['id']['S']
                },
                UpdateExpression='SET City = :val1, Country = :val2, Temperature = :val3, Humidity = :val4, Pressure = :val5',
                ExpressionAttributeValues={
                    ':val1': results['name'],
                    ':val2': results['sys']['country'],
                    ':val3': Decimal(str(results['main']['temp'])),
                    ':val4': Decimal(str(results['main']['humidity'])),
                    ':val5': Decimal(str(results['main']['pressure']))
                }
            )