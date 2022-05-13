import {Accordion, Col} from "react-bootstrap";
import TransactionViewComponent from "./transactionViewComponent";

const AccountViewComponent = (props) => {
    const {account} = props;

    const sortTransaction = (transaction_a, transaction_b) => {
        const date_a = new Date(transaction_a.created_at);
        const date_b = new Date(transaction_b.created_at);
        return date_a < date_b ? 1 : -1;
    }
    const transactions = account.income_transactions.concat(account.outcome_transactions);
    transactions.sort(sortTransaction);

    return <Accordion.Item eventKey={account.id}>
        <Accordion.Header style={{alignItems: "center"}}>
            <Col className={'text-start'}>{account.account_number}</Col>
            <Col className={'text-end me-2'}>{account.balance}</Col>
        </Accordion.Header>
        <Accordion.Body>
            {transactions.map(el => {
                const transactionType = el.dest_account_id.toString() === account.id.toString() ? "in" : "out";
                return <TransactionViewComponent
                    transaction={el}
                    transactionType={transactionType}
                />
            })
            }
        </Accordion.Body>
    </Accordion.Item>
}

export default AccountViewComponent;