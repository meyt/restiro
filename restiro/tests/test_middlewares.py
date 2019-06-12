import pytest

from os.path import join

from webtest.debugapp import debug_app

from restiro import DocumentationRoot, clean_examples_dir
from restiro.tests.helpers import package_dir, mockup_resources

examples_dir = join(package_dir, 'examples')


@pytest.fixture('session', autouse=True)
def wrap_directories():
    clean_examples_dir()
    yield


def test_webtest_middleware():
    from restiro.middlewares.webtest import TestApp

    # Initiate test app (middleware)
    test_app = TestApp(
        app=debug_app
    )

    # Default request with no documentation
    test_app.get('/too/far/away')

    # Simple request
    test_app.doc = True
    test_app.get('/far/away')

    test_app.doc = True
    test_app.get('/user', 'a=b').mustcontain('a=b')

    # Fill examples by request
    test_app.doc = True
    test_app.get('/user')

    # JSON request
    test_app.doc = True
    test_app.post_json('/user', {
        'full_name': 'Meyti'
    })

    test_app.doc = True
    test_app.post_json('/user?status=400+Bad+name', {
        'full_name': 'Meyti2'
    }, status=400)

    # Initiate documentation root
    docs_root = DocumentationRoot(
        title='Hello World'
    )
    docs_root.resources.extend(mockup_resources())
    docs_root.load_resource_examples()

    resource = docs_root.resources.find(path='/user', method='get')
    assert len(resource.examples) == 2
    assert resource.examples[0].response.status == 200
    assert resource.examples[0].response.body_format is None

    # JSON Request
    resource = docs_root.resources.find(path='/user', method='post')
    assert 'Meyti' in resource.examples[0].request.__repr__()
    assert 'Meyti' in resource.examples[0].response.__repr__()
    assert 'content-type' in resource.examples[0].request.headers
    assert resource.examples[1].response.reason == 'Bad name'

    resource = docs_root.resources.find(path='/user/1/image/1', method='get')
    assert resource.__str__() == 'GET /user/:user_id/image/:image_id'

    resource = docs_root.resources.find(path='/user/1/image', method='get')
    assert resource.__str__() == 'GET /user/:user_id/image'

    resource = docs_root.resources.find(path='/user/1', method='get')
    assert resource.__str__() == 'GET /user/:user_id'

    # Unicode
    test_app.post('/user', upload_files=[
        ('file', 'file.bin', b'')
    ])
