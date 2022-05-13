import * as React from "react";
import {BrowserRouter, Route, Routes, Navigate} from "react-router-dom";
import {AuthProvider, useAuth} from "./components/authProvider";
import RequireAuth from "./components/RequireAuth";
import LoginPage from "./pages/LoginPage";
import HomePage from "./pages/HomePage";
const AppRoutes = () => {
    return (
        <AuthProvider>
            <BrowserRouter>
                <Routes>
                    <Route path="/"
                           element={<Navigate to="/home"/>}
                    />
                    <Route path="/login" element={<LoginPage/>}/>
                    <Route path="/signup" element={<LoginPage/>}/>
                    <Route path="/home" element={<RequireAuth><HomePage/></RequireAuth>}/>
                </Routes>
            </BrowserRouter>
        </AuthProvider>
    );
};

export default AppRoutes;