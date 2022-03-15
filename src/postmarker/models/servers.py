from django.conf import settings
from .base import Model, ModelManager



class Servers(Model):
    def __str__(self):
        return "{}: {} ({})".format(
            self.__class__.__name__,
            self._data.get("Name"),
            self._data.get("ID"),
        )

    def get(self):
        new_instance = self._manager.get(self.ID)
        self._data = new_instance._data
        return self

    def edit(self, **kwargs):
        response = self._manager.edit(self.ID, **kwargs)
        self._update(response)

    def delete(self):
        return self._manager.delete(self.ID)


class ServersManager(ModelManager):
    name = "servers"
    model = Servers
    token_type = "account"

    def get(self, id):
        response = self.call("GET", "/servers/%s" % id)
        return self._init_instance(response)

    def create(self, Name, **kwargs):
        data = {"Name": Name, **kwargs}
        return self._init_instance(self.call("POST", "/servers", data=data))

    def edit(self, id, **kwargs):
        return self.call("PUT", "/servers/%s" % id, data=kwargs)

    def all(self, count=500, offset=0, **kwargs):
        responses = self.call_many("GET", "/servers", count=count, offset=offset, **kwargs)
        return self.expand_responses(responses, "Servers")

    def delete(self, id):
        return self.call("DELETE", "/servers/%s" % id)["Message"]
