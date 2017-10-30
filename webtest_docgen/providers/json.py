import json
from . import BaseProvider


class JSONProvider(BaseProvider):

    def get_resource_filename(self, resource):
        return '%s.json' % super().get_resource_filename(resource)

    def get_index_filename(self):
        return '%s.json' % super().get_index_filename()

    def generate_resources(self):
        pass

    def write_resource(self, file_stream, resource):
        pass

    def write_index(self, file_stream):
        file_stream.write(json.dumps(self.docs_root.to_dict()))
