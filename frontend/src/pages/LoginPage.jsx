import {Container, Row, Col, Form, Button} from "react-bootstrap";
import {useState} from "react";
import {Link} from "react-router-dom";
import getAxiosClient from "../utils/axiosClient";
import ToastNotification from "../components/toastNotification";
import {useAuth} from "../components/authProvider";
import {useNavigate} from "react-router-dom";

function LoginPage() {
    const auth = useAuth();
    const [isAuthenticating, setIsAuthenticating] = useState(false);
    const [loginError, setLoginError] = useState(undefined);
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();

    const handleLogin = async () => {
        const axios = getAxiosClient();
        setIsAuthenticating(true);
        try {
            const response = await axios.post("sign-in", {
                email: username,
                password: password
            });
            auth.login(response.data?.token);
            navigate("/home")
        } catch (err) {
            console.log(err);
            if (err.response?.status === 401) {
                setLoginError("Incorrect email or/and password")
            } else {
                setLoginError("Something went wrong, try again later")
            }
        }
        setIsAuthenticating(false);
    }

    return (
        <Container>

            {loginError && <ToastNotification
                notificationType='error'
                notificationMessage={loginError}
                onClose={() => {
                    setLoginError(undefined);
                }}
            />}

            <Row className="justify-content-md-center py-4">
                <Col xs lg="4" md="auto" className={"text-center"}>
                    <h2>
                        MTransfer login
                    </h2>
                </Col>
            </Row>
            <Form>
                <Row className="justify-content-md-center py-2">
                    <Col xs lg="4" md="auto">
                        <Form.Group className="mb-3" controlId="username">
                            <Form.Text className="text-muted">
                                Email/Username
                            </Form.Text>
                            <Form.Control
                                disabled={isAuthenticating}
                                onChange={e => setUsername(e.target.value)}
                                type="email"
                                value={username}
                                placeholder="Enter email"
                            />
                        </Form.Group>
                    </Col>
                </Row>
                <Row className="justify-content-md-center pt-2">
                    <Col xs lg="4" md="auto">
                        <Form.Group className="mb-3" controlId="password">
                            <Form.Text className="text-muted">
                                Password
                            </Form.Text>
                            <Form.Control
                                disabled={isAuthenticating}
                                type="password"
                                value={password}
                                onChange={e => setPassword(e.target.value)}
                                placeholder="Enter password"/>
                        </Form.Group>
                    </Col>
                </Row>
                <Row className="justify-content-md-center pt-4 text-center">
                    <Col xs lg="4" md="auto">
                        <Button
                            onClick={e => handleLogin()}
                            disabled={isAuthenticating}
                            size='lg'>
                            <span className='px-3'>Continue</span>
                        </Button>
                    </Col>
                </Row>
            </Form>
            <Row className="justify-content-md-center text-center py-5">
                <Col xs lg="4" md="auto">
                    <span>Don't have an account?</span><br/>
                    <Link className='text-muted' to={'/signup'}>Sign up</Link>
                </Col>
            </Row>
        </Container>
    );
}

export default LoginPage;
