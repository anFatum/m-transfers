import * as React from "react";
import {createContext, useContext} from "react";
import {useLocalStorage} from "use-hooks";
import getAxiosClient from "../utils/axiosClient";

const AuthContext = createContext(null);


export const AuthProvider = ({children}) => {
    const [token, setAuthToken] = useLocalStorage("token", undefined);
    const [user, setUser] = React.useState(undefined);

    React.useEffect(() => {
        if (!token)
            return;
        const axios = getAxiosClient();
        axios.get("user").then(response => {
                setUser(response.data);
            }
        )
    }, [token])

    const login = (token) => {
        setAuthToken(token);
    };

    const logout = () => {
        setAuthToken(undefined);
    };

    const value = {
        token,
        login,
        logout,
        user
    };

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    return useContext(AuthContext);
}