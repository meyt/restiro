"""
    @api {post} /media Upload a media file
    @apiVersion 1.0.0
    @apiGroup Media

    @apiPermission god
    @apiPermission supervisor
    @apiPermission operator
    @apiPermission user

    @apiParam {File} file this file is useful
                        for some reason
                        or maybe not
    @apiParam {Boolean} [visible] this is test
    @apiParam {String} something

    @apiDescription this is a description
                    for test this api

                    and
                    some
                    other

                    this
                    is 1
    @apiDescription this is 2
    @apiDescription overwritten
                    for test this api

                    and
                    some
                    other
                    things

    @apiSuccess {String} ideas

    @apiUse CommissionReportSuccess

"""

expected_dict = {
    'method': 'post',
    'path': '/media',
    'title': 'Upload a media file',
    'version': '1.0.0',
    'group': 'Media',
    'permission': ('god', 'supervisor', 'operator', 'user'),
    'param': ({'name': 'file',
               'optional': False,
               'type': 'File'},

              {'name': 'visible',
               'optional': True,
               'type': 'Boolean'})
}
