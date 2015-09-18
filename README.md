# Webpy Thermostat

## Overview

This web server lets you monitor and update a few (fake) thermostats in a home.

## Installing
In order to run you will need to install web.py

     sudo easy_install web.py
     python server.py

## API

### List thermostats
  ***GET*** /thermostats (http://localhost:8080/thermostats)


  Accepted Parameters:


  fields: a comma separated list of field names you with to query
          ie. http://localhost:8080/thermostats?fields=name,operating_mode


          accepted fields: name, temperature, operating_mode, fan_mode, ID, cool_point, heat_point
          If an unknown field is given, a 422 Unprocessable Entity error is returned


  Returns: a JSON list of Thermostat dictionaries


  Sample return value:

     curl localhost:8080/thermostats
     [{
         name: "thermostat 1",
         temperature: 62,
         operating_mode: "cool",
         fan_mode: "auto",
         ID: 1,
         cool_point: 76,
         heat_point: 62
      },
      {
         name: "thermostat 2",
         temperature: 73,
         operating_mode: "heat",
         fan_mode: "auto",
         ID: 2,
         cool_point: 77,
         heat_point: 63
      }]

### Individual thermostats
  ***GET*** /thermostats/thermostat_id (http://localhost:8080/thermostats/1)


  Accepted Parameters:


  * fields: a comma separated list of field names to filter results
            ie. http://localhost:8080/thermostats/1?fields=name,operating_mode


          accepted fields: name, temperature, operating_mode, fan_mode, ID, cool_point, heat_point
          If an unknown field is given, a 422 Unprocessable Entity error is returned

  Returns: a JSON Thermostat dictionary

  Sample return value:

       curl localhost:8080/thermostats/1
       {
          name: "thermostat 1",
          temperature: 62,
          operating_mode: "cool",
          fan_mode: "auto",
          ID: 1,
          cool_point: 76,
          heat_point: 62
       }

       curl localhost:8080/thermostats/1?fields=name
       {
          name: "thermostat 1",
       }


***PATCH*** /thermostats/thermostat_id (http://localhost:8080/thermostats/1)

  Accepted Parameters: None

  Accepted data: partial JSON Thermostat

  * updateable fields:
    * name: string
    * operating_mode: string. accepted values: "cool", "heat", "off"
    * fan_mode: string. accepted values: "off", "auto"
    * cool_point: int. accepted range: 30 <= value <= 100
    * heat_point: int. accepted range: 30 <= value <= 100

  sample PATCH data:

       {
          name: "Living Room",
          operating_mode: "off",
          fan_mode: "off",
       }


  Returns: No data
