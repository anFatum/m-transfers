import {Toast, ToastContainer} from 'react-bootstrap';

const ToastNotification = (props) => {

    const notificationConfig = (notificationType) => {
        switch (notificationType) {
            case "error":
                return {
                    bg: "danger",
                    className: 'text-white',
                    title: "Error occurred"
                }
            case "success":
                return {
                    bg: "success",
                    className: 'text-white',
                    title: "Success!"
                }
            default:
                return {
                    bg: "danger",
                    className: 'text-white'
                }
        }
    }
    const config = notificationConfig(props.notificationType)

    return (
        <ToastContainer className="p-3" position='top-end'>
            <Toast
                className="d-inline-block m-1" bg={config.bg}
                onClose={() => {
                    props.onClose()
                }}
                autohide={true}
            >
                <Toast.Header>
                    <strong className="me-auto">{config.title}</strong>
                    <small>Just now</small>
                </Toast.Header>
                <Toast.Body className={config.className}>
                    {props.notificationMessage}
                </Toast.Body>
            </Toast>
        </ToastContainer>
    )
}

export default ToastNotification;