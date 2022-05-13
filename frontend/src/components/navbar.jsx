import {Navbar, Col, Container, Nav} from "react-bootstrap";
import {useAuth} from "./authProvider";
import {useNavigate} from "react-router-dom";

const MNavbar = () => {
    const auth = useAuth();
    const navigate = useNavigate();

    return <Navbar bg="light" expand="lg">
        <Container>
            <Navbar.Collapse id="basic-navbar-nav">
                <Nav className="ms-auto">
                    <Nav.Link disabled={true}>Hello, {auth.user?.email}</Nav.Link>
                    <Nav.Link onClick={() => {
                        auth.logout();
                        navigate("/")
                    }}>Logout</Nav.Link>
                </Nav>
            </Navbar.Collapse>
        </Container>
    </Navbar>
}

export default MNavbar;