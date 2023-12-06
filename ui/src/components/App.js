import React from "react"
import { Routes, Route } from 'react-router-dom';
import RegisterForm from "./RegisterForm";
import Dashboard1 from "./Dashboard1";
import LoginForm from "./LoginForm";
import FiltersComponent from "./FiltersComponent";



const App = () =>  {
    return (
        <Routes>
            <Route path="/" element={(<FiltersComponent/>)}/>
            <Route path="/register" element={(<RegisterForm/>)}/>
            <Route path="/login" element={(<LoginForm/>)}/>
            <Route path="/numeric-statistics" element={(<Dashboard1/>)}/>
        </Routes>
    )

}

export default App