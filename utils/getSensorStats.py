import pandas as pd
from decimal import Decimal
import boto3
from boto3.dynamodb.conditions import Attr

def lambda_handler(event, context):
    '''
    This function will be triggered twice a day to update some sensor statistics.
    '''

    dynamodb = boto3.resource('dynamodb')
    tableMeasures = dynamodb.Table('sensors-hist')
    tableSensor = dynamodb.Table('sensors-data')
 
    sensorList = tableSensor.scan()
  
    for sensor in sensorList['Items']:
        measures = tableMeasures.scan(
            FilterExpression=Attr('id').begins_with(sensor['id'])
        )
        
        data = pd.DataFrame({
            'date': [ aMeasure['Date'] for aMeasure in measures['Items']],
            'temperature': [ aMeasure['Temperature'] for aMeasure in measures['Items']],
            'humidity': [ aMeasure['Humidity'] for aMeasure in measures['Items']]
        })

        stats = {
            'temperature':  {
                'min': str(data['temperature'].min()),
                'max': str(data['temperature'].max()),
                'mean': str(data['temperature'].mean()),
            },
            'humidity':  {
                'min': str(data['humidity'].min()),
                'max': str(data['humidity'].max()),
                'mean': str(data['humidity'].mean()),
            },
            'advanced': {
                'covariance': str(data.temperature.astype('float64').cov(data.humidity.astype('float64'))),
                'correlation': str(data.temperature.astype('float64').corr(data.humidity.astype('float64')))
            }
        }

        tableSensor.update_item(
            Key={
                'id': sensor['id']
            },
            UpdateExpression='SET SensorStats = :val1',
            ExpressionAttributeValues={
                ':val1': stats
            }
        )
