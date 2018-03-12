'use strict';

const uuid = require('uuid/v1')
const aws = require('aws-sdk')
const dynamoDb = new aws.DynamoDB.DocumentClient()
const table = 'sensors-data'

/**
 * Adds a new sensor to the database
 * @param {The event containing json data from the call} event 
 * @param {not used} context 
 * @param {Necessary when using lambda with API Gateway} callback 
 */
module.exports.addSensor = (event, context, callback) => {

    const data = JSON.parse(event.body)
    if (typeof data.name != 'string' || typeof data.lat != 'number' || typeof data.lng != 'number') {
        console.error('Create: Type validation failed')
        callback(new Error('data validation error'))
        return
    }

    const params = {
        TableName: table,
        Item: {
            id: uuid(),
            SensorName: data.name,
            SensorLatitude: data.lat,
            SensorLongitude: data.lng,
            City: '-',
            Country: '-',
            Humidity: '-',
            Pressure: '_',
            Temperature: '-',
            SensorStats: {
                'temperature':  {
                    'min': '-',
                    'max': '-',
                    'mean': '-',
                },
                'humidity':  {
                    'min': '-',
                    'max': '-',
                    'mean': '-',
                },
                'advanced': {
                    'covariance': '-',
                    'correlation': '-'
                }
            }
        }
    }

    dynamoDb.put(params, (err, results) => {
        if (err) {
            console.error(err)
            callback(err)
            return
        }

        callback(null, {
            statusCode: 200,
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': '*',
              },
            body: JSON.stringify({ 'results': 'ok' })
        })
    })
}

/**
 * Get a list with all sensors and basic statistics data
 * @param {The event containing json data from the call} event 
 * @param {not used} context 
 * @param {Necessary when using lambda with API Gateway} callback 
 */
module.exports.listSensors = (event, context, callback) => {

    const params = {
        TableName: table
    }

    dynamoDb.scan(params, (err, results) => {
        if (err) {
            console.error(err)
            callback(err)
            return
        }

        const response = {
            statusCode: 200,
            headers: {
                "Access-Control-Allow-Origin": "*"
            },
            body: JSON.stringify(results.Items)
        }

        callback(null, response)
    })
}