from app.core.parsers.request_parsers import pagination_parser

transaction_filter_parser = pagination_parser.copy()

transaction_filter_parser.add_argument('origin_account_id',
                                       help="account number",
                                       type=str,
                                       required=False)

transaction_filter_parser.add_argument('dest_account_id',
                                       help="account owner id",
                                       type=str,
                                       required=False)
