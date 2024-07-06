import React, { useContext } from "react";
import { Navigate } from "react-router-dom";
import UserContext from "../auth/UserContext";

function PrivateRoute({ element }) {
    const { currentUser } = useContext(UserContext);

    console.debug("PrivateRoute", "currentUser=", currentUser);

    if (!currentUser) {
        return <Navigate to="/login" />;
    }

    return element;
}

export default PrivateRoute;
