import {Button, Col, Container, Form, Row} from "react-bootstrap";
import {useState} from "react";
import {Link, useNavigate} from "react-router-dom";
import getAxiosClient from "../utils/axiosClient";
import ToastNotification from "../components/toastNotification";

function SignupPage() {
    const [isAuthenticating, setIsAuthenticating] = useState(false);
    const [signupError, setSignupError] = useState("");
    const [signupForm, setSignupForm] = useState({
        email: "",
        name: "",
        password: "",
        admin: false
    })
    const navigate = useNavigate();

    const handleLogin = async () => {
        const axios = getAxiosClient();
        setIsAuthenticating(true);
        try {
            const response = await axios.post("users", {
                ...signupForm,
                roles: signupForm.admin ? ["admin"] : ['app_user']
            });
            navigate("/login")
        } catch (err) {
            console.log(err);
            setSignupError("Something went wrong, try again later");
        }
        setIsAuthenticating(false);
    }

    return (
        <Container>
            {signupError && <ToastNotification
                notificationType='error'
                notificationMessage={signupError}
                onClose={() => {
                    setSignupError(undefined);
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
                                Email
                            </Form.Text>
                            <Form.Control
                                disabled={isAuthenticating}
                                onChange={e => setSignupForm({...signupForm, email: e.target.value})}
                                type="email"
                                value={signupForm.email}
                                placeholder="Enter email"
                            />
                        </Form.Group>
                    </Col>
                </Row><Row className="justify-content-md-center py-2">
                <Col xs lg="4" md="auto">
                    <Form.Group className="mb-3" controlId="username">
                        <Form.Text className="text-muted">
                            Name
                        </Form.Text>
                        <Form.Control
                            disabled={isAuthenticating}
                            onChange={e => setSignupForm({...signupForm, name: e.target.value})}
                            type="email"
                            value={signupForm.name}
                            placeholder="Enter name"
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
                                value={signupForm.password}
                                onChange={e => setSignupForm({...signupForm, password: e.target.value})}
                                placeholder="Enter password"/>
                        </Form.Group>
                    </Col>
                </Row>
                <Row className="justify-content-md-center pt-2">
                    <Col xs lg="4" md="auto">
                        <Form.Check
                            type='checkbox'
                            id='agreeTermsOfUsage'
                        >
                            <Form.Check.Input
                                disabled={isAuthenticating}
                                type='checkbox'
                                value={signupForm.admin}
                                onChange={e => setSignupForm({...signupForm, admin: e.target.value})}
                            />
                            <Form.Check.Label>
                                Admin account?
                            </Form.Check.Label>
                        </Form.Check>
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
        </Container>
    );
}

export default SignupPage;
