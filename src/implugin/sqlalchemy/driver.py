from sqlalchemy.orm.exc import NoResultFound


class Driver(object):

    def feed_request(self, request):
        self.request = request

    @property
    def query(self):
        return self.database().query

    @property
    def database(self):
        return self.request.database


class ModelDriver(Driver):

    def upsert(self, **kwargs):
        try:
            return self.query(self.model).filter_by(**kwargs).one()
        except NoResultFound:
            return self.create(**kwargs)

    def get_by_id(self, id):
        return self.find_all().filter_by(id=id).one()

    def find_all(self):
        return self.query(self.model)

    def find_by(self, **kwargs):
        return self.query(self.model).filter_by(**kwargs)

    def create(self, **kwargs):
        obj = self.model()
        for key, value in kwargs.items():
            setattr(obj, key, value)
        self.database().add(obj)
        return obj

    def delete_by_id(self, id_):
        self.delete(self.get_by_id(id_))

    def delete(self, obj):
        self.database().delete(obj)

