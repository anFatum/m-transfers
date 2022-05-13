import {Alert} from "react-bootstrap";

const TransactionViewComponent = (props) => {
    const {transaction, transactionType} = props;

    const transactionConfig = (type) => {
        switch (type) {
            case "out":
                return {
                    bg: "danger"
                }
            case "in":
                return {
                    bg: "success"
                }
            default:
                return {
                    bg: "dark"
                }
        }
    }
    const config = transactionConfig(transactionType);

    return <Alert variant={config.bg}>
        <Alert.Heading>{transaction.amount}</Alert.Heading>
        <p>Comment: {transaction.comment || "No comment provided"}</p>
        <p>Date: {transaction.created_at}</p>
    </Alert>
}

export default TransactionViewComponent;