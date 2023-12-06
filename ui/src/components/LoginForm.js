import React, {useState, useEffect} from "react"
import axios from "axios";
import './stylesheets/LoginForm.css'
import {Navigate, NavLink} from "react-router-dom";
import {setAuthToken} from "../authentication";
import {InputDiv} from "./RegisterForm";


const LoginForm = () => {
    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")
    const [isAuthorised, setIsAuthorised] = useState(false)
    const [errorMsg, setErrorMsg] = useState("")

    const sendRequest = async (event) => {
        event.preventDefault()

        const formData = new FormData()
        formData.append('username', username)
        formData.append('password', password)

        await axios.post("http://localhost/login", formData, {
            headers: {
                'content-type': 'application/json'
            }
        })
            .then((response) => {
                if (response) {
                    if (response.status === 201) {
                    localStorage['access_token'] = response.data['access_token']
                    setAuthToken(response.data['access_token'])
                    localStorage['refresh_token'] = response.data['refresh_token']
                    setIsAuthorised(true)
            }
        }})
            .catch((e) => setErrorMsg(e.response.data.message))
    }

    useEffect(() => {

    }, [isAuthorised])

    if (isAuthorised) {
        return <Navigate to={"/"}/>
    }

    return (
        <div className="LoginForm container">
            <div className={"row mt-5"}>
                <div className={"col-lg-4 bg-white m-auto"}>
                    <h2 className={"text-center pt-3"}>Sign in</h2>
                    <p className={"text-center text-muted lead"}>Doesn't have an account yet? <NavLink to={"/register"}>Sing up</NavLink></p>
                    <form onSubmit={sendRequest}>
                        <InputDiv
                            labelText={"Username"}
                            type={"text"}
                            id_={"InputUsername"}
                            onChangeFn={(e) => {setErrorMsg("");
                                setUsername(e)}}
                            description={"Enter your username"}
                        />

                        <InputDiv
                            labelText={"Password"}
                            type={"password"}
                            id_={"InputPassword"}
                            onChangeFn={(e) => {
                                setErrorMsg("")
                                setPassword(e)
                            }}
                            description={"Enter your username"}
                        />
                        {errorMsg && <div className="alert alert-danger mb-3" role="alert">{errorMsg}</div>}

                        <button type={"submit"}  className="btn btn-primary">Sing in</button>
                    </form>
                </div>


            </div>


        </div>
    )

}

export default LoginForm