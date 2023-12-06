import axios from "axios";



export const setAuthToken = token => {
    if (token) {
        axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
    } else
        delete axios.defaults.headers.common["Authorization"];
}
export const clearTokens = () => {
    localStorage['access_token'] = ""
    localStorage['refresh_token'] = ""
    setAuthToken("")
}
const refreshToken = () => {
    axios.post("http://localhost:80/refresh", {"refresh_token": localStorage.getItem("refresh_token")})
        .then((res) => {
            localStorage['access_token'] = res.data['access_token']
            localStorage['refresh_token'] = res.data['refresh_token']
            setAuthToken(res.data['access_token'])
        })
        .catch(() => {
            localStorage['access_token'] = ""
            localStorage['refresh_token'] = ""
            setAuthToken("")
        })
    return !!localStorage['refresh_token']
}

export default refreshToken