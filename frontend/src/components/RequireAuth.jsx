import * as React from "react";
import {Navigate, useLocation,} from "react-router-dom";
import {useAuth} from "./authProvider";

const RequireAuth = ({children}) => {
    const auth = useAuth();
    let location = useLocation();

    if (!auth?.token) {
        return <Navigate to="/login" state={{from: location}} replace/>;
    }

    return children;
}

export default RequireAuth;