import React from "react"
import { Routes, Route } from 'react-router-dom';
import Register from "./Register";
import Dashboard1 from "./Dashboard1";
import LoginForm from "./LoginForm";
import FiltersComponent from "./FiltersComponent";



const App = () =>  {
    return (
        <Routes>
            <Route path="/" element={(<FiltersComponent/>)}/>
            <Route path="/register" element={(<Register/>)}/>
            <Route path="/login" element={(<LoginForm/>)}/>
            <Route path="/numeric-statistics" element={(<Dashboard1/>)}/>
        </Routes>
    )

}

export default App