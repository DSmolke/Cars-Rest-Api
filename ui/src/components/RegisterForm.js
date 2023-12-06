import React, {useState} from "react"
import axios from "axios";
import {Link, NavLink} from "react-router-dom";
import "bootstrap-icons/font/bootstrap-icons.css";

const SuccessfulRegister = () =>
    <div className={"container d-flex align-items-center h-100"}>
        <div className={"w-100"}>
            <p className={"text-center"}><i className="bi h1 bi-building-fill-check mr-auto ml-auto"></i></p>
            <h3 className={"text-center"}>Verification email was sent! Please check your mailbox</h3>
            <p className={"text-center mt-5"}>
                Already verified? <Link to={"/login"} className={"text-center"}>Log in</Link>
            </p>
        </div>
    </div>

const FormHeader = () => {
    return (
        <span>
            <h2 className={"text-center pt-3"}>Create account</h2>
            <p className={"text-center text-muted lead"}>It's Fast! Get access to the platform</p>
            <p className={"text-center text-muted lead mb-4"}>Already have an account? <NavLink
                to={"/login"}>Sing in</NavLink></p>
        </span>)
}

export const InputDiv = ({labelText, type, id_, description, onChangeFn}) => {
    return (
        <div className="mb-3">
            <label htmlFor={id_} className="form-label">{labelText}</label>
            <input type={type} className="form-control" id={id_}
                   aria-describedby="usernameHelp" onChange={(e) => onChangeFn(e.target.value)}/>
            {description && <div id={`${id_}Help`} className="form-text">{description}</div>}
        </div>
    )
}

const RegisterForm = () => {
    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")
    const [email, setEmail] = useState("")
    const [role, setRole] = useState("")
    const [errorMsg, setErrorMsg] = useState("")
    const [isCreated, setIsCreated] = useState(false)

    const sendRequest = async (event) => {
        event.preventDefault()

        const formData = new FormData()
        formData.append('username', username)
        formData.append('password', password)
        formData.append('email', email)
        formData.append('role', role)

        await axios.post("http://localhost/users", formData, {headers: {'content-type': 'application/json'}})
            .then(() => setIsCreated(true))
            .catch(err => setErrorMsg(err.response.data.message))
    }
    if (isCreated) {
        return (<SuccessfulRegister/>)
    }

    return (
        <div className="RegisterForm container">
            <div className={"row mt-5"}>
                <div className={"col-lg-4 bg-white m-auto"}>
                    <FormHeader/>
                    <form onChange={() => setErrorMsg("")} onSubmit={sendRequest}>
                        <InputDiv
                            labelText={"Username"}
                            type={"text"}
                            id_={"InputUsername"}
                            description={"Enter your username"}
                            onChangeFn={setUsername}
                        />
                        <InputDiv
                            labelText={"Password"}
                            type={"password"}
                            id_={"InputPassword"}
                            onChangeFn={setPassword}
                        />
                        <InputDiv
                            labelText={"Email"}
                            type={"email"}
                            id_={"inputEmail"}
                            onChangeFn={setEmail}
                        />
                        <InputDiv
                            labelText={"Role"}
                            type={"text"}
                            id_={"v"}
                            onChangeFn={setRole}
                        />

                        {errorMsg && <div className="alert alert-danger mb-3" role="alert">{errorMsg}</div>}

                        <button type={"submit"} className="btn btn-primary mt-1">Submit</button>
                    </form>
                </div>
            </div>
        </div>
    )
}

export default RegisterForm