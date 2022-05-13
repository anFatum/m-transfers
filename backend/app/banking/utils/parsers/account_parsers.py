from backend.app.core.parsers.request_parsers import pagination_parser

account_filter_parser = pagination_parser.copy()

account_filter_parser.add_argument('account_number',
                                   help="account number",
                                   type=str,
                                   required=False)

account_filter_parser.add_argument('owner_id',
                                   help="account owner id",
                                   type=str,
                                   required=False)
