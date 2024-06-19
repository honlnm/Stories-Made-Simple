import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import LoginForm from "../auth/LoginForm";
import ProfileForm from "../profiles/ProfileForm";
import PlotList from "../plots/PlotList";
import SignupForm from "../auth/SignupForm";
import PrivateRoute from "./PrivateRoute";


function Routing({ login, signup }) {
    console.debug(
        "Routes",
        `login=${typeof login}`,
        `register=${typeof register}`,
    );

    return (
        <div className="pt-5">
            <Routes>
                <Route exact path="/login" element={<LoginForm login={login} />} />
                <Route exact path="/signup" element={<SignupForm signup={signup} />} />
                <Route path="/profile" element={<PrivateRoute element={<ProfileForm />} />} />
                <Route path="/dashboard" element={<PrivateRoute element={<PlotList />} />} />
                <Route path="*" element={<Navigate to="/" />} />
            </Routes>
        </div>
    );
}

export default Routing;