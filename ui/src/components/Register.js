import React, {useEffect, useRef, useState} from "react"

import axios from "axios";
import {Link, NavLink} from "react-router-dom";
import "bootstrap-icons/font/bootstrap-icons.css";
import {faCheck, faTimes, faInfoCircle} from "@fortawesome/free-solid-svg-icons"
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";

const USER_REGEX = /^[a-zA-Z0-9_]{3,20}$/
const PWD_REGEX = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/
const EMAIL_REGEX = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
const ROLE_REGEX = /^(USER)|(ADMIN)$/

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

const Register = () => {
    const userRef = useRef()

    const [user, setUser] = useState('')
    const [validName, setValidName] = useState(false)
    const [userFocus, setUserFocus] = useState(false)

    const [password, setPassword] = useState('')
    const [validPassword, setValidPassword] = useState(false)
    const [passwordFocus, setPasswordFocus] = useState(false)

    const [matchPassword, setMatchPassword] = useState('')
    const [validMatchPassword, setValidMatchPassword] = useState(false)
    const [matchPasswordFocus, setMatchPasswordFocus] = useState(false)

    const [email, setEmail] = useState('')
    const [validEmail, setValidEmail] = useState(false)
    const [emailFocus, setEmailFocus] = useState(false)

    const [role, setRole] = useState('')
    const [validRole, setValidRole] = useState(false)
    const [roleFocus, setRoleFocus] = useState(false)

    const [errMsg, setErrMsg] = useState('')
    const [success, setSuccess] = useState(false)

    const [loading, setLoading] = useState(false)

    useEffect(() => {
        userRef.current.focus()
    }, []);

    useEffect(() => {
        const result = USER_REGEX.test(user)
        setValidName(result)
    }, [user]);

    useEffect(() => {
        const result = PWD_REGEX.test(password)
        setValidPassword(result)
        const match = password === matchPassword
        setValidMatchPassword(match)
    }, [password, matchPassword]);

    useEffect(() => {
        const result = EMAIL_REGEX.test(email)
        setValidEmail(result)
    }, [email]);

    useEffect(() => {
        const result = ROLE_REGEX.test(role)
        setValidRole(result)
    }, [role]);

    useEffect(() => {
        setErrMsg('')
    }, [user, password, matchPassword, email, role]);

    useEffect(() => {
        setLoading(false)
    }, [errMsg]);

    const sendRequest = async (event) => {
        event.preventDefault()
        const [userValidation, pwdValidation] = [USER_REGEX.test(user), PWD_REGEX.test(password)]
        if (!userValidation || !pwdValidation) {
            setErrMsg("Invalid credential")
        } else {
            const formData = new FormData()
            formData.append('username', user)
            formData.append('password', password)
            formData.append('email', email)
            formData.append('role', role)

            await axios.post("http://localhost/users", formData, {headers: {'content-type': 'application/json'}})
                .then((res) => res.status === 201 ? setSuccess(true) : setErrMsg('Problem'))
                .catch(err => setErrMsg(err.response?.data ? err.response.data.message : "Something went wrong"))
        }
    }

    return (
        <>
            {success ? (<SuccessfulRegister/>) : (
                <div className="RegisterForm container">
                    <div className={"row mt-5"}>
                        <div className={"col-lg-4 bg-white m-auto"}>
                            <FormHeader/>
                            <section>
                                {errMsg && <div className="alert mb-3" role="alert">{errMsg}</div>}
                                <form onSubmit={sendRequest}>

                                    <label htmlFor="username">
                                        Username:
                                        <span className={validName ? "valid" : "hide"}>
                        <FontAwesomeIcon icon={faCheck}/>
                    </span>
                                        <span className={validName || !user ? "hide" : "invalid"}>
                        <FontAwesomeIcon icon={faTimes}/>

                    </span>

                                    </label>
                                    <input
                                        className={'form-control'}
                                        type="text"
                                        id="username"
                                        ref={userRef}
                                        autoComplete={"off"}
                                        onChange={(e) => setUser(e.target.value)}
                                        required
                                        aria-invalid={validName ? "false" : "true"}
                                        aria-describedby="uidnote"
                                        onFocus={() => setUserFocus(true)}
                                        onBlur={() => setUserFocus(false)}
                                    />
                                    <p id="uidnote"
                                       className={userFocus && user && !validName ? "instructions" : "offscreen"}>
                                        <FontAwesomeIcon icon={faInfoCircle}/>
                                        3 to 24 characters.<br/>
                                        Must begin with a letter.<br/>
                                        Letters, numbers, underscores allowed.
                                    </p>

                                    {/*    ----------------------------------- PASSWORD -------------------------------------------------*/}
                                    <label htmlFor="password">
                                        Password:
                                        <span className={validPassword ? "valid" : "hide"}>
                        <FontAwesomeIcon icon={faCheck}/>
                    </span>
                                        <span className={validPassword || !password ? "hide" : "invalid"}>
                        <FontAwesomeIcon icon={faTimes}/>
                    </span>
                                    </label>
                                    <input
                                        className={'form-control'}
                                        type="password"
                                        id="password"
                                        onChange={(e) => setPassword(e.target.value)}
                                        required
                                        aria-invalid={validName ? "false" : "true"}
                                        aria-describedby="pwdnote"
                                        onFocus={() => setPasswordFocus(true)}
                                        onBlur={() => setPasswordFocus(false)}
                                    />
                                    <p id="pwdnote"
                                       className={passwordFocus && password && !validPassword ? "instructions" : "offscreen"}>
                                        <FontAwesomeIcon icon={faInfoCircle}/>
                                        At least 8 alphanumeric characters<br/>
                                    </p>

                                    {/*    ----------------------------------- CONFIRM PASSWORD -------------------------------------------------*/}
                                    <label htmlFor="confirm_pwd">
                                        Confirm Password:
                                        <span className={validMatchPassword && matchPassword ? "valid" : "hide"}>
                        <FontAwesomeIcon icon={faCheck}/>
                    </span>
                                        <span className={validMatchPassword || !matchPassword ? "hide" : "invalid"}>
                        <FontAwesomeIcon icon={faTimes}/>
                    </span>
                                    </label>
                                    <input
                                        className={'form-control'}
                                        type="password"
                                        id="confirm_pwd"
                                        onChange={(e) => setMatchPassword(e.target.value)}
                                        required
                                        aria-invalid={validMatchPassword ? "false" : "true"}
                                        aria-describedby="confirmnote"
                                        onFocus={() => setMatchPasswordFocus(true)}
                                        onBlur={() => setMatchPasswordFocus(false)}
                                    />
                                    <p id="confirmnote"
                                       className={matchPasswordFocus && !validMatchPassword ? "instructions" : "offscreen"}>
                                        <FontAwesomeIcon icon={faInfoCircle}/>
                                        Must match the first password input field<br/>
                                    </p>

                                    {/*    ----------------------------------- EMAIL -------------------------------------------------*/}
                                    <label htmlFor="email">
                                        Email:
                                        <span className={validEmail ? "valid" : "hide"}>
                        <FontAwesomeIcon icon={faCheck}/>
                    </span>
                                        <span className={validEmail || !email ? "hide" : "invalid"}>
                        <FontAwesomeIcon icon={faTimes}/>
                    </span>
                                    </label>
                                    <input
                                        className={'form-control'}
                                        type="email"
                                        id="email"
                                        onChange={(e) => setEmail(e.target.value)}
                                        required
                                        aria-invalid={validName ? "false" : "true"}
                                        aria-describedby="emailnote"
                                        onFocus={() => setEmailFocus(true)}
                                        onBlur={() => setEmailFocus(false)}
                                    />
                                    <p id="emailnote"
                                       className={emailFocus && email && !validEmail ? "instructions" : "offscreen"}>
                                        <FontAwesomeIcon icon={faInfoCircle}/>
                                        At least 5 characters<br/>
                                        One @ is needed<br/>
                                        Special characters are allowed<br/>
                                    </p>

                                    {/*    ----------------------------------- Role -------------------------------------------------*/}
                                    <label htmlFor="role">
                                        Role:
                                        <span className={validRole ? "valid" : "hide"}>
                        <FontAwesomeIcon icon={faCheck}/>
                    </span>
                                        <span className={validRole || !role ? "hide" : "invalid"}>
                        <FontAwesomeIcon icon={faTimes}/>
                    </span>
                                    </label>
                                    <input
                                        className={'form-control'}
                                        type="text"
                                        id="role"
                                        onChange={(e) => setRole(e.target.value)}
                                        required
                                        aria-invalid={validName ? "false" : "true"}
                                        aria-describedby="rolenote"
                                        onFocus={() => setRoleFocus(true)}
                                        onBlur={() => setRoleFocus(false)}
                                    />
                                    <p id="rolenote"
                                       className={roleFocus && role && !validRole ? "instructions" : "offscreen"}>
                                        <FontAwesomeIcon icon={faInfoCircle}/>
                                        ADMIN or USER<br/>

                                    </p>

                                    {/*    ----------------------------------- Button -------------------------------------------------*/}
                                    <button className={"btn btn-primary"} onClick={() => setLoading(true)}
                                            disabled={!validName || !validPassword || !validPassword || !validMatchPassword || !validRole}
                                    >{!loading ? "Sign up" : <div className="spinner-border" role="status">
                                        <span className="visually-hidden">Loading...</span>
                                    </div>}
                                    </button>
                                </form>

                            </section>
                        </div>
                    </div>
                </div>
            )}

        </>

    )
}

export default Register