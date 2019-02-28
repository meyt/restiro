import json

from restiro.generators import BaseGenerator


class JSONGenerator(BaseGenerator):

    def get_index_filename(self):
        return '%s.json' % super().get_index_filename()

    def generate_documents(self):
        pass

    def generate_resources(self):
        pass

    def write_resource(self, file_stream, resource):  # pragma: nocover
        pass

    def write_document(self, file_stream, document):  # pragma: nocover
        pass

    def write_index(self, file_stream):
        file_stream.write(json.dumps(self.docs_root.to_dict()))
