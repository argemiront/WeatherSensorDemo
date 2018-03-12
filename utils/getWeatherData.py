import http.client
import json
import boto3
from decimal import Decimal
import keys
import datetime

def lambda_handler(event, context):
    '''
    This function will be called every hour to fetch new weather 
    data for each sensor station.
    '''

    dynamodb = boto3.resource('dynamodb')
    tableMeasures = dynamodb.Table('sensors-hist')
    tableSensor = dynamodb.Table('sensors-data')
 
    sensorItems = tableSensor.scan()
    
    base = keys.BASE
    key = keys.KEY
    units = keys.UNITS
    
    apiConn = http.client.HTTPConnection(base)
    
    for record in sensorItems['Items']:
        lat = str(record['SensorLatitude'])
        lng = str(record['SensorLongitude'])
        url = '/data/2.5/weather?lat=' + lat + '&lon=' + lng + units + key
        apiConn.request('GET', url)
        r1 = apiConn.getresponse()
        results = json.loads(r1.read())
            
        tableMeasures.put_item(
            Item={
                'id': str(record['id'] + datetime.datetime.now().strftime("%Y-%m-%d&%H:%M:%S")),
                'SensorID': record['id'],
                'Date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'Temperature': Decimal(str(results['main']['temp'])),
                'Humidity': Decimal(str(results['main']['humidity']))
            }
        )
        
        tableSensor.update_item(
            Key={
                'id': record['id']
            },
            UpdateExpression='SET Temperature = :val1, Humidity = :val2',
            ExpressionAttributeValues={
                ':val1': Decimal(str(results['main']['temp'])),
                ':val2': Decimal(str(results['main']['humidity']))
            }
        )