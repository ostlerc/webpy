import web, json

from thermostat import Thermostat

UnprocessableEntity = lambda data: web.HTTPError('422 Unprocessable Entity', {'Content-Type':'text/plain'}, data)
BadRequest = lambda data: web.HTTPError('400 Bad Request', {'Content-Type':'text/plain'}, data)

class ThermostatHandler:
    """ThermostatHandler handles GET for all thermostats
    field filtering available"""

    def GET(self):
        params = web.input(fields=None)
        try:
            return json.dumps(Thermostat.all(), default=lambda o: o.json(params.fields), indent=4)
        except KeyError as e:
            raise UnprocessableEntity('invalid field {}'.format(e))

class SingleThermostatHandler:
    """SingleThermostatHandler handles any specific thermostat resource GET or PATCH Request
    field filtering available for GET"""

    def GET(self, ID):
        params = web.input(fields=None)
        try:
            thermostat = Thermostat.find(int(ID))
            if thermostat is None:
                raise web.notfound()

            return json.dumps(thermostat, default=lambda o: o.json(params.fields), indent=4)
        except KeyError as e:
            raise UnprocessableEntity('invalid field {}'.format(e))


    def PATCH(self, ID):
        thermostat = Thermostat.find(int(ID))
        if thermostat is None:
            raise web.notfound()

        # parse and validate patch input data
        try:
            fields = json.loads(web.data())
        except ValueError:
            raise BadRequest("invalid JSON")

        if not isinstance(fields, dict):
            raise BadRequest("invalid JSON")

        # validate all keys are correct before mutating
        for field in fields:
            if not isinstance(field, basestring):
                raise BadRequest("invalid JSON")
            if not hasattr(thermostat, field) or field in ['temperature','ID']:
                raise UnprocessableEntity('invalid field {}'.format(field))

        try:
            for field in fields:
                setattr(thermostat, field, fields[field])
        except TypeError:
            raise UnprocessableEntity('invalid type for field {}'.format(field))
        except ValueError:
            raise UnprocessableEntity('invalid value for field {}'.format(field))

        return ''

if __name__ == "__main__":
    urls = (
        '/thermostats', 'ThermostatHandler',
        '/thermostats/(\d+)', 'SingleThermostatHandler'
    )

    app = web.application(urls, globals())
    app.run()
