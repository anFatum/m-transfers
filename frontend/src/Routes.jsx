import * as React from "react";
import {BrowserRouter, Navigate, Route, Routes} from "react-router-dom";
import {AuthProvider} from "./components/authProvider";
import RequireAuth from "./components/RequireAuth";
import LoginPage from "./pages/LoginPage";
import HomePage from "./pages/HomePage";
import SignupPage from "./pages/SignUpPage";

const AppRoutes = () => {
    return (
        <AuthProvider>
            <BrowserRouter>
                <Routes>
                    <Route path="/"
                           element={<Navigate to="/home"/>}
                    />
                    <Route path="/login" element={<LoginPage/>}/>
                    <Route path="/signup" element={<SignupPage/>}/>
                    <Route path="/home" element={<RequireAuth><HomePage/></RequireAuth>}/>
                </Routes>
            </BrowserRouter>
        </AuthProvider>
    );
};

export default AppRoutes;