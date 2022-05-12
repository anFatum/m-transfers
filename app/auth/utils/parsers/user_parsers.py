from app.core.parsers.request_parsers import pagination_parser

user_filter_parser = pagination_parser.copy()

user_filter_parser.add_argument('email',
                                help="User email",
                                type=str,
                                required=False)
