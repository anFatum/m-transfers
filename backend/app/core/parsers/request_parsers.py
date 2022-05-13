from flask_restplus import reqparse

authentication_parser = reqparse.RequestParser()
authentication_parser.add_argument('Authorization', location='headers',
                                   type=str,
                                   help='Bearer Access Token')

pagination_parser = authentication_parser.copy()
pagination_parser.add_argument('page',
                               help="Pagination page",
                               type=int,
                               required=False,
                               default=1)
pagination_parser.add_argument('per_page',
                               help="Items per page",
                               type=int,
                               required=False,
                               choices=[5, 10, 20, 30, 40, 50])
