# RESTiro

[![Build Status](
    https://travis-ci.org/meyt/restiro.svg?branch=master
)](
    https://travis-ci.org/meyt/restiro
) 
[![Coverage Status](
    https://coveralls.io/repos/github/meyt/restiro/badge.svg?branch=master
)](
    https://coveralls.io/github/meyt/restiro?branch=master
)

RESTful API documentation generator (inline documentation + tests)


## Features

- [x] Inline documentation parser
- [x] Example recorder middleware
- [x] Generate documentation in Markdown 
- [x] Generate documentation in HTML 
[[restiro-spa-material](https://github.com/meyt/restiro-spa-material)]


## Install

```
    pip install restiro
```

## Usage

1. Describe the request in comments, e.g:
    
    controller/shelf.py
    ```python
    class ShelfController:
        
        def post(self):
            """
            @api {post} /shelf/:shelfId/book Add book into shelf
    
            @apiVersion 1
            @apiGroup Book
            @apiPermission Noneres
            
            @apiParam {String} title
            @apiParam {String} author
            @apiParam {DateTime} [publishDate]
             
            @apiDescription 
            Here is some description
            with full support of markdown.
            
            - watch this!
            - and this!
            - there is a list!
            """
            return [11, 22, 33]
    ```
    

2. Attach `restiro` middleware to your WSGI/HTTP verifier
    (currently `webtest` supported), e.g:
    
    Your project tests initializer:
    
    ```python
    from restiro.middlewares.webtest import TestApp
    from restiro import clean_examples_dir
    
    from my_project import wsgi_app
    
    clean_examples_dir()
    test_app = TestApp(wsgi_app)
    
    ```

3. Define responses to capture, e.g:

    ```python
    
    def test_shelf(test_app):
        test_app.get('/shelf/100/book')
        
        test_app.delete('/shelf/121/book')
        
        test_app.doc = True
        test_app.post(
            '/shelf/100/book',
            json={
                'title': 'Harry Potter',
                'author': 'JK. Rowling'
            }
        )
        
        test_app.doc = True
        test_app.post(
            '/shelf/100/book',
            json={
                'title': 'Harry Potter2'
            },
            status=400
        )
    ```
        
4. Run tests
5. Build documentation 
    
    ```
    $ restiro a_library
    ```

    Response will be something like: 
    
    shelf-{shelf_id}-book-post.md
    ```markdown
        #  Add book into shelf
        
        ## `POST` `/shelf/:shelfId/book`
        
        Here is some description
        with full support of markdown.
        
        - watch this!
        - and this!
        - there is a list!
        
        
        ## Parameters
        
        ### Form parameters
        
        Name | Type | Required | Default | Example | enum | Pattern | MinLength | MaxLength | Minimum | Maximum | Repeat | Description
        --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---
        title | String | `True` |  |  |  |  |  |  |  |  | `False` | 
        author | String | `True` |  |  |  |  |  |  |  |  | `False` | 
        publishDate | DateTime | `False` |  |  |  |  |  |  |  |  | `False` | 
        
        ## Examples
        
        ### 200 OK
        
        #### Request: 
        
        ```
        POST /shelf/100/book
        Content-Type: application/x-www-form-urlencoded
        ```
        ```
        title=Harry Potter
        author=JK. Rowling
        ```
        
        #### Response: 
        
        ```
        Content-Type: application/json
        ```
        ```
        [11, 22, 33]
        ```
        
        
        ### 400 Bad Request, missed parameter `author`
        
        #### Request: 
        
        ```
        POST /shelf/100/book
        Content-Type: application/x-www-form-urlencoded
        ```
        ```
        title=Harry Potter2
        ```
        
        #### Response: 
        
        ```
        Content-Type: application/json
        ```
        ```
        {"message": "Missed parameter `author`"}
        ```
        
        ---
    ```
    
    
## CLI

```
usage: restiro [-h] [-t TITLE] [-o OUTPUT] [-b BASE_URI]
               [-g {markdown,json,spa_material,mock}] [-l LOCALES]
               [--build-gettext [BUILD_GETTEXT]]
               src

Restiro Builder

positional arguments:
  src                   Project module name

optional arguments:
  -h, --help            show this help message and exit
  -t TITLE, --title TITLE
                        Project title
  -o OUTPUT, --output OUTPUT
                        Output directory
  -b BASE_URI, --base-uri BASE_URI
                        Base URI
  -g {markdown,json,spa_material,mock}, --generator {markdown,json,spa_material,mock}
                        Generator, default: markdown
  -l LOCALES, --locales LOCALES
                        Locales directory
  --build-gettext [BUILD_GETTEXT]
                        Build .POT templates
```
