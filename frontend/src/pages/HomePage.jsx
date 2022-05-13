import {Col, Container, Row, Button, Accordion} from "react-bootstrap";
import {useState, useEffect} from "react";
import {useAuth} from "../components/authProvider";
import getAxiosClient from "../utils/axiosClient";
import AccountViewComponent from '../components/accountViewComponent'
import MNavbar from "../components/navbar";

function HomePage() {

    const [accountList, setAccountList] = useState(undefined);
    const [transactions, setTransactions] = useState({});
    const [isLoading, setIsLoading] = useState(false);
    const auth = useAuth();

    const refetchAccounts = async () => {
        if (auth.user) {
            const axios = getAxiosClient();
            const response = await axios.get("accounts", {params: {owner_id: auth.user.id}});
            setAccountList(response.data);
        }
    }

    useEffect(() => {
        refetchAccounts();
    }, [auth])

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
                                            accountList.map(account => {
                                                console.log(account);
                                                return <AccountViewComponent account={account}/>
                                            })
                                        }
                                    </Accordion>
                                }
                            </Col>
                        </Row>
                    </Container>
                </Col>
                <Col lg="4">
                    <Container >
                        <Row className="text-end">
                            <Col>
                                <Button
                                    onClick={onOpenAccountButtonClick}
                                >
                                    Open new account
                                </Button>
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
