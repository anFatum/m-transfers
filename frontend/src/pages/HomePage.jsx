import {Col, Container, Row, Button, Accordion} from "react-bootstrap";
import {useState, useEffect} from "react";
import {useAuth} from "../components/authProvider";
import getAxiosClient from "../utils/axiosClient";
import AccountViewComponent from '../components/accountViewComponent'
import MNavbar from "../components/navbar";
import MakeTransactionViewComponent from "../components/makeTransactionComponent";

function HomePage() {

    const [accountList, setAccountList] = useState(undefined);
    const auth = useAuth();

    const refetchAccounts = async () => {
        if (auth.user) {
            const axios = getAxiosClient();
            try {
                const response = await axios.get("accounts", {params: {owner_id: auth.user.id}});
                auth.setUser({...auth.user, accounts: response.data})
                setAccountList(response.data);
            } catch (e) {
                setAccountList([]);
            }
        }
    }

    useEffect(() => {
        refetchAccounts();
    }, [auth.user?.id])

    const onOpenAccountButtonClick = async () => {
        const axios = getAxiosClient();
        const response = await axios.post("accounts", {});
        await refetchAccounts();
    }

    return (
        <>
            <MNavbar/>
            <Container>
                <Row className="justify-content-md-center py-4">
                    <Col xs lg="4" md="auto" className={"text-center"}>
                        <h2>
                            Home page
                        </h2>
                    </Col>
                </Row>

                <Row>
                    <Col lg="8">
                        <Container>
                            <Row>
                                <Col>
                                    {accountList &&
                                        <Accordion>
                                            {
                                                accountList.map(account => <AccountViewComponent account={account}/>)
                                            }
                                        </Accordion>
                                    }
                                </Col>
                            </Row>
                        </Container>
                    </Col>
                    <Col lg="4">
                        <Container>
                            <Row className="text-end">
                                <Col>
                                    <Button
                                        onClick={onOpenAccountButtonClick}
                                    >
                                        Open new account
                                    </Button>
                                </Col>
                            </Row>
                            <Row className={"pt-4"}>
                                <Col>
                                    <MakeTransactionViewComponent
                                        onSuccess={refetchAccounts}
                                    />
                                </Col>
                            </Row>
                        </Container>
                    </Col>
                </Row>
            </Container>
        </>
    );
}

export default HomePage;
