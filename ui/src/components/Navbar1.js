import React from "react"
import {Link, NavLink} from "react-router-dom";

import {clearTokens} from "../authentication";



const Navbar1 = () => {

    return (
        <div>
        <nav className="navbar navbar-expand-lg bg-light">
            <div className="container-fluid">
                <a className="navbar-brand" href="src#"><img src="https://pierwszy-bucket-2.s3.eu-central-1.amazonaws.com/samochody_01/logo.jpg" alt="Bootstrap" width="50" height="50"/></a>
                <button className="navbar-toggler" type="button" data-bs-toggle="collapse"
                        data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent"
                        aria-expanded="false" aria-label="Toggle navigation">
                    <span className="navbar-toggler-icon"></span>
                </button>
                <div className="collapse navbar-collapse" id="navbarSupportedContent">
                    <ul className="navbar-nav me-auto mb-2 mb-lg-0">
                        <li className="nav-item">
                            <NavLink to={"/"} className="nav-link active" aria-current="page">Main page</NavLink>
                        </li>
                        <li className="nav-item">
                            {/*<NavLink to={"#"} className="nav-link">Dodaj pojazd</NavLink>*/}
                        </li>
                        <li className="nav-item dropdown">
                            <a className="nav-link dropdown-toggle" role="button" data-bs-toggle="dropdown"
                               aria-expanded="false">
                                Statistics
                            </a>
                            <ul className="dropdown-menu">
                                <li><NavLink to={"numeric-statistics"} className="dropdown-item" href="#">Numeric attributes</NavLink></li>
                            </ul>
                        </li>
                    </ul>

                    <div className="d-flex justify-content-center" role="search">
                        <Link onClick={() => clearTokens()} to={'/login'} className="btn btn-danger auth-btn" role="button">Log out</Link>

                    </div>
                </div>
            </div>
        </nav>
        <nav className="navbar navbar-light bg-light .form-inline">
        </nav>
        </div>
    )
}

export default Navbar1