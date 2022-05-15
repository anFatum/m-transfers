import {Container, Row, Col, Form, Button} from "react-bootstrap";
import {useState, useEffect} from "react";
import getAxiosClient from "../utils/axiosClient";
import {useAuth} from "./authProvider";

const MakeTransactionViewComponent = (props) => {

    const auth = useAuth();
    const [users, setUsers] = useState([]);
    const [selectedUser, setSelectedUser] = useState(undefined);
    const [amount, setAmount] = useState(0);
    const [comment, setComment] = useState("");
    const [selectedFromAcc, setSelectedFromAcc] = useState(undefined);
    const [selectedDestAcc, setSelectedDestAcc] = useState(undefined);
    const [isLoading, setIsLoading] = useState(false);

    useEffect(() => {
        const axios = getAxiosClient();
        axios.get("users").then(response => {
            setUsers(response.data);
            setSelectedUser(response.data[0]);
        });
    }, [])

    useEffect(() => {
        if (auth.user && auth.user.accounts) {
            if (auth.user.accounts[0])
                setSelectedFromAcc(auth.user.accounts[0].id)
        }
    }, [auth.user])

    useEffect(() => {
        if (selectedUser && selectedUser.accounts) {
            if (selectedUser.accounts[0])
                setSelectedDestAcc(selectedUser.accounts[0].id)
        }
    }, [selectedUser])

    const handleTransfer = async () => {
        const axios = getAxiosClient();
        setIsLoading(true);
        try {
            const response = await axios.post("transactions", {
                origin_account_id: Number(selectedFromAcc),
                dest_account_id: Number(selectedDestAcc),
                amount: amount,
                comment: comment,
            });
            await props.onSuccess();
        } catch (err) {
            console.log(err);
        }
        setIsLoading(false);
    }
    if (!auth.user){
        return <></>
    }

    return <Container>
        <Row>
            <h5 style={{textAlign: "right"}}>Make transaction</h5>
            <Col>
                <Form.Label>Account you want to transfer: </Form.Label>
                <Form.Select aria-label="Select account you want to transfer funds"
                             disabled={isLoading}
                             onChange={e => setSelectedFromAcc(e.target.value)}>
                    {auth.user && auth.user.accounts && auth.user.accounts.map(account => (<option
                        key={account.id}
                        value={account.id}>
                        {account.account_number}
                    </option>))}
                </Form.Select>
            </Col>
        </Row>
        <Row className={"pt-3"}>
            <Col>
                <Form.Label>User to transfer: </Form.Label>
                <Form.Select aria-label="Select user to transfer funds"
                             disabled={isLoading}
                             onChange={e => {
                                 const userId = e.target.value;
                                 const selectedUser = users.find(user => user.id.toString() === userId.toString());
                                 setSelectedUser(selectedUser);
                             }
                             }>
                    {users && users.map(user => {
                        if (user.id !== auth.user.id)
                            return (<option
                                key={user.id}
                                value={user.id}>
                                {user.name}
                            </option>)
                    })}
                </Form.Select>
            </Col>
        </Row>
        <Row style={{textAlign: "right"}} className={"pt-3"}>
            <Col>
                <Form.Select aria-label="Select account to transfer funds"
                             disabled={isLoading}
                             onChange={e => setSelectedDestAcc(e.target.value)}>
                    {selectedUser && selectedUser.accounts &&
                        selectedUser.accounts.map(account => (<option
                            key={account.id}
                            value={account.id}>
                            {account.account_number}
                        </option>))}
                </Form.Select>
            </Col>
        </Row>
        <Row className={"pt-3"}>
            <Col>
                <Form.Group className="mb-3" controlId="username">
                    <Form.Label>
                        Transfer Amount:
                    </Form.Label>
                    <Form.Control
                        disabled={isLoading}
                        onChange={e => setAmount(Number(e.target.value))}
                        type="number"
                        value={amount}
                        placeholder="Enter amount"
                    />
                </Form.Group>
            </Col>
        </Row>
        <Row className={"pt-3"}>
            <Col>
                <Form.Group className="mb-3" controlId="username">
                    <Form.Label>
                        Comment (optional):
                    </Form.Label>
                    <Form.Control
                        disabled={isLoading}
                        onChange={e => setComment(e.target.value)}
                        type="text"
                        value={comment}
                        placeholder="Enter comment (optional)"
                    />
                </Form.Group>
            </Col>
        </Row>
        <Row className="justify-content-md-center pt-4 text-center">
            <Col xs lg="4" md="auto">
                <Button
                    onClick={e => handleTransfer()}
                    disabled={isLoading}
                    size='lg'>
                    <span className='px-3'>Submit</span>
                </Button>
            </Col>
        </Row>
    </Container>
}

export default MakeTransactionViewComponent;