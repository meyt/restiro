import shutil

from os import makedirs
from os.path import exists, dirname, join

from webtest_docgen import DocumentationRoot, Resource, Document


class BaseProvider:
    _files = []

    def __init__(self, docs_root: DocumentationRoot, destination_dir):
        self.destination_dir = destination_dir
        self.docs_root = docs_root

    def _ensure_file(self, filename):
        filename = join(self.destination_dir, filename)
        d = dirname(filename)
        if not exists(d):
            makedirs(d)

        if filename in self._files:
            return open(filename, 'a')
        else:
            f = open(filename, 'w')
            self._files.append(filename)
            return f

    def generate_resources(self):
        for resource_path, resource_methods in self.docs_root.resources.__tree__.items():
            for resource_method, resources in resource_methods.items():
                for resource in resources:
                    f = self._ensure_file(self.get_resource_filename(resource))
                    self.write_resource(f, resource)
                    f.close()

    def generate_documents(self):
        for document in self.docs_root.documents:
            f = self._ensure_file(self.get_document_filename(document))
            self.write_document(f, document)
            f.close()

    def generate_index(self):
        f = self._ensure_file(self.get_index_filename())
        self.write_index(f)
        f.close()

    def clean_destination(self):
        shutil.rmtree(self.destination_dir)

    def get_resource_filename(self, resource: Resource):
        return "%s" % resource.__filename__

    def get_document_filename(self, document: Document):
        return "-%s" % document.__filename__

    def get_index_filename(self):
        return 'index'

    def write_document(self, file_stream, document):
        raise NotImplementedError

    def write_resource(self, file_stream, resource):
        raise NotImplementedError

    def write_index(self, file_stream):
        raise NotImplementedError

    def generate(self):
        self.clean_destination()
        self.generate_documents()
        self.generate_resources()
        self.generate_index()
