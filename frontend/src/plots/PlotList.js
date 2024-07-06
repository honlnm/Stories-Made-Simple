import React, { useState, useContext } from "react";
import Alert from "../common/Alert";
import StoriesMadeSimpleApi from "../api/api";
import UserContext from "../auth/UserContext";

function PlotList() {
    const { currentUser, setCurrentUser } = useContext(UserContext);
    const [plotList, setPlotList] = useState([]);
    const [formErrors, setFormErrors] = useState([]);

    console.debug(
        "ProfileForm",
        "currentUser=", currentUser,
        "plotList=", plotList,
        "formErrors=", formErrors,
    );

    return (
        <div className="col-md-6 col-lg-4 offset-md-3 offset-lg-4">
            <h3>Dashboard</h3>
            <div className="card">
                <div className="card-body">
                    <ul>

                    </ul>
                </div>
            </div>
        </div>
    );
}

export default PlotList;