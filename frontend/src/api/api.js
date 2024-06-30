import axios from "axios";

const BASE_URL = process.env.REACT_APP_BASE_URL || "http://127.0.0.1:5000";

class StoriesMadeSimpleApi {
    static token;

    static async request(endpoint, data = {}, method = "get") {
        console.debug("API Call:", endpoint, data, method);

        const url = `${BASE_URL}/${endpoint}`;
        const headers = { Authorization: `Bearer ${StoriesMadeSimpleApi.token}` };
        const params = (method === "get")
            ? data
            : {};

        try {
            return (await axios({ url, method, data, params, headers })).data;
        } catch (err) {
            console.error("API Error:", err.response);
            let message = err.response.data.error.message;
            throw Array.isArray(message) ? message : [message];
        }
    }

    // Individual API routes


    /** Get token for login from username, password. */
    static async login(data) {
        let res = await this.request(`auth/token`, data, "post");
        return res.token;
    }

    /** Signup for site. */
    static async signup(data) {
        let res = await this.request(`auth/signup`, data, "post");
        return res.token;
    }

    /**Get the current user */
    static async getCurrentUser(user_id) {
        let res = await this.request(`users/${user_id}`);
        return res.user;
    }

    /** Update user profile info */
    static async updateProfile(user_id, data) {
        let res = await this.request(`users/${user_id}/edit`, data, "patch");
        return res.user;
    }

    /**Get Plottig Frameworks, filtered by name if not undefined */

    /**Get Plot Points from Framework */

    /**Get Series Types, filtered by name if not undefined */

    /**Get Genres, filtered by name if not undefined */

    /**Get current user's plots */
    static async getCurrentUserPlots(username) {
        let res = await this.request(``)
        return res.plots;
    }

    /**Get current user's plot point from user's plot */
    static async getPlotPoints(username, plot_id) {
        let res = await this.request(``)
        return res.plot_points;
    }

    /**Create Series/Plot(s) */


}

export default StoriesMadeSimpleApi;