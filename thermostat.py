
class Thermostat(object):
    "Thermostat encapsulates the data model for a single home thermostat"

    _id = 0
    # thermostats is the in memory list of all thermostats
    thermostats = []

    def __init__(self, name, operating_mode, cool_point, heat_point, fan_mode):
        """__init__ constructs the thermostat and sets member variables appropriately

        Parameters
        ----------
        ID: integer
            unique read only system identifier
        name: string
            read-write display name
            value must be non empty
        operating_mode: string
            read-write human readable text of the current operating mode
            valid values: "cool", "heat", "off"
        cool_point: int
            read-write value between 30-100 degrees fahrenheit
        heat_point: int
            read-write value between 30-100 degrees fahrenheit
        fan_mode: string
            read-write human readable text of the current fan model
            valid values: "off", "auto"

        Exceptions
        ----------
        TypeError or ValueError can be thrown with invalid input"""

        self._objs = {'ID' : self._new_id()}
        self.name = name
        self.operating_mode = operating_mode
        self.cool_point = cool_point
        self.heat_point = heat_point
        self.fan_mode = fan_mode

    @property
    def ID(self):
        """id returns the read only unique id for the thermostat"""
        return self._objs['ID']

    def json(self, fields):
        """json returns the thermostat data as a dictionary.
        a new random temperature is added as the 'temperature' key

        Parameters
        ----------
        fields: string
            a comma separated list of field names that should be returned
            If None, all fields are returned
        """
        data = self._objs.copy()
        data['temperature'] = self.temperature
        if fields is not None:
            data = {fld: data[fld] for fld in fields.split(',')}
        return data

    @property
    def temperature(self):
        from random import randint
        return randint(60,90)

    @property
    def name(self):
        return self._objs['name']

    @name.setter
    def name(self, value):
        if not isinstance(value, basestring):
            raise TypeError("name")
        if value == "":
            raise ValueError("empty name")
        self._objs['name'] = value

    @property
    def operating_mode(self):
        return self._objs['operating_mode']

    @operating_mode.setter
    def operating_mode(self, value):
        if not isinstance(value, basestring):
            raise TypeError("operating_mode")
        if value not in ["cool", "heat", "off"]:
            raise ValueError("invalid operating_mode state")
        self._objs['operating_mode'] = value

    @property
    def cool_point(self):
        return self._objs['cool_point']

    @cool_point.setter
    def cool_point(self, value):
        if not isinstance(value, int):
            raise TypeError("cool_point")
        if not 30 <= value <= 100:
            raise ValueError("cool_point")
        self._objs['cool_point'] = value

    @property
    def heat_point(self):
        return self._objs['heat_point']

    @heat_point.setter
    def heat_point(self, value):
        if not isinstance(value, int):
            raise TypeError("heat_point")
        if not 30 <= value <= 100:
            raise ValueError("heat_point")
        self._objs['heat_point'] = value

    @property
    def fan_mode(self):
        return self._objs['fan_mode']

    @fan_mode.setter
    def fan_mode(self, value):
        if not isinstance(value, basestring):
            raise TypeError("fan_mode")
        if not value in ["off", "auto"]:
            raise ValueError("invalid fan_mode state")
        self._objs['fan_mode'] = value

    def _new_id(self):
        """_new_id returns the next available ID for a thermostat"""
        Thermostat._id += 1
        return Thermostat._id

    @classmethod
    def all(cls):
        """all returns all the known thermostats in a list
        This would normally come from a database, but we just store in memory for now"""
        if len(cls.thermostats) == 0:
            cls.thermostats.append(
                Thermostat(name="thermostat 1", operating_mode="cool", cool_point=76, heat_point=62, fan_mode="auto"))
            cls.thermostats.append(
                Thermostat(name="thermostat 2", operating_mode="heat", cool_point=77, heat_point=63, fan_mode="auto"))

        return Thermostat.thermostats

    @classmethod
    def find(cls, ID):
        """find returns the thermostat with the given ID
        returns None if it could not be found

        Parameters
        ----------
        ID: integer
            unique read only system identifier"""
        if not isinstance(ID, int):
            raise TypeError("id")
        try:
            return next(t for t in Thermostat.all() if t.ID == ID)
        except StopIteration:
            return None
