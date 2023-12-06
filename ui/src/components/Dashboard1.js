import React, {useState, useEffect} from "react"
import axios from "axios";
import Navbar1 from "./Navbar1";
import refreshToken from "../authentication";
import {Navigate} from "react-router-dom";

const SingleStatisticCard = ({name, color, value}) => {
    return (
        <div className={`col-3 statistic-card rounded bg-${color}`}>
            <h2 className={"text-center"}>{name}</h2>
            <h3 className={"text-center"}>{value}</h3>
        </div>
    )
}
const SingleStatistic = ({name, data}) => {
    return (
        <div className={"row statistic-element-header"}>
            <div className={"col-12"}>
                <h1 className={"text-center"}>{name}</h1>
            </div>
            <div className={"row d-flex justify-content-between cards-keeper"}>
                <SingleStatisticCard color={"primary"} name={"Average"} value={data["avg"]}/>
                <SingleStatisticCard color={"success"} name={"Max"} value={data["max"]}/>
                <SingleStatisticCard color={"danger"} name={"Min"} value={data["min"]}/>
            </div>
        </div>
    )
}
const Dashboard1 = () => {

    const [url, setUrl] = useState("http://localhost:80/cars/numeric_field_statistics/price&mileage")
    const [dataPrice, setDataPrice] = useState({})
    const [dataMileage, setDataMileage] = useState({})

    useEffect(() => {
        const fetchData = async () => {

            const response = await axios.get(url, {"headers": {"Authorization": `Bearer ${localStorage['access_token']}`}})
                .then(response => {
                        setDataPrice(response.data.price)
                        setDataMileage(response.data.mileage)
                    }
                )
                .catch(err => console.log(err))
        }
        fetchData()
    }, [])

    if (!refreshToken()) {
        return (<Navigate to={"/login"}/>)

    }
    return (
        <div>
            <Navbar1/>
            <div className={"container"}>
                <SingleStatistic
                    name={"Vehicles prices"}
                    data={dataPrice}
                />
                <SingleStatistic
                    name={"Vehicle mileages"}
                    data={dataMileage}
                />
            </div>
        </div>

    )
}

export default Dashboard1