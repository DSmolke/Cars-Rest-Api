import React, {useState, useEffect} from "react";
import CarsList from "./CarsList";
import axios from "axios";
import Navbar1 from "./Navbar1";
import {Navigate} from "react-router-dom";
import refreshToken from "../authentication";


const FiltersComponent = () => {

    const [attribute, setAttribute] = useState('price')
    const [order, setOrder] = useState('desc')
    const [url, setUrl] = useState("http://localhost:80/cars/all")
    const [cars, setCars] = useState([])
    const [minPrice, setMinPrice] = useState(0)
    const [maxPrice, setMaxPrice] = useState(1000000)
    const [priceOrder, setPriceOrder] = useState("ASC")
    const [color, setColor] = useState("")

    const fetchData = async () => {

        const response = await axios.get(url, {"headers": {"Authorization": `Bearer ${localStorage['access_token']}`}})
            .catch(err => console.log(err))
        const data = await response?.data

        if (data instanceof Array) {
            setCars(data)
        } else if (data instanceof Object) {
            setCars(data[color])
        }

    }

    useEffect(() => {
        refreshToken()

    }, [])

    useEffect(() => {

        fetchData()
    }, [url])

    if (refreshToken() === false) {
        return (<Navigate to={"/login"}/>)
    } else {

    return (<div>
            <Navbar1/>
            <div className={"container"}>
                <div className={"row"}>
                    <div className={"col-12"}>Filters:</div>
                </div>


                <div className={"row"}>
                    <div className={"col-lg-2"}>
                        <button onClick={() => setUrl("http://localhost:80/cars/with_sorted_components")} type="button"
                                className="btn btn-primary f-btn">
                            Sort components
                        </button>
                    </div>
                    <div className={'col-lg-2'}>
                        <button type="button" class="btn btn-primary f-btn" data-bs-toggle="modal"
                                data-bs-target="#exampleModal">
                            Attributes
                        </button>
                    </div>

                    <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel"
                         aria-hidden="true">
                        <div class="modal-dialog">
                            <div class="modal-content">
                                <div class="modal-header">
                                    <h1 class="modal-title fs-5" id="exampleModalLabel">Attribute filter</h1>
                                    <button type="button" class="btn-close" data-bs-dismiss="modal"
                                            aria-label="Close"></button>
                                </div>
                                <div class="modal-body">
                                    <h5>Attribute</h5>
                                    <select onChange={(event) => setAttribute(event.target.value)}
                                            className="form-control form-control-lg">
                                        <option value={"model"}>Model</option>
                                        <option value={"price"}>Price</option>
                                        <option value={"color"}>Color</option>
                                        <option value={"mileage"}>Mileage</option>
                                        <option value={"components"}>Equipment</option>
                                    </select>
                                    <h5>Sort</h5>
                                    <select onChange={(event) => setOrder(event.target.value)}
                                            className="form-control form-control-lg">
                                        <option value={"desc"}>Descending</option>
                                        <option value={"asc"}>Ascending</option>
                                    </select>
                                </div>
                                <div class="modal-footer">
                                    <button onClick={() => {
                                        setUrl(`http://localhost:80/cars/all/${attribute}/${order}`)

                                    }

                                    } type="button" class="btn btn-primary" data-bs-dismiss="modal">Filter
                                    </button>
                                </div>


                            </div>

                        </div>
                    </div>
                    {/*End modal*/}
                    <div className={'col-lg-2'}>
                        <button type="button" class="btn btn-primary f-btn" data-bs-toggle="modal"
                                data-bs-target="#Modal1">
                            Color
                        </button>
                    </div>

                    <div class="modal fade" id="Modal1" tabindex="-1" aria-labelledby="Modal1Label"
                         aria-hidden="true">
                        <div class="modal-dialog">
                            <div class="modal-content">
                                <div class="modal-header">
                                    <h1 class="modal-title fs-5" id="Modal1Label"></h1>
                                    <button type="button" class="btn-close" data-bs-dismiss="modal"
                                            aria-label="Close"></button>
                                </div>
                                <div class="modal-body">
                                    <h5>Select color</h5>
                                    <select onChange={(event) => setColor(event.target.value)}
                                            className="form-control form-control-lg">
                                        <option value={"white"}>White</option>
                                        <option value={"black"}>Black</option>
                                        <option value={"red"}>Red</option>
                                        <option value={"green"}>Green</option>
                                        <option value={"blue"}>Blue</option>
                                        <option value={"pink"}>Pink</option>
                                        <option value={"orange"}>Orange</option>
                                        <option value={"silver"}>Silver</option>
                                    </select>

                                </div>
                                <div class="modal-footer">
                                    <button onClick={() => {
                                        setUrl(`http://localhost:80/cars/colors_map?color=${color}`)
                                    }
                                    } type="button" class="btn btn-primary" data-bs-dismiss="modal">Filter
                                    </button>
                                </div>


                            </div>

                        </div>
                    </div>
                    {/*End modal*/}
                    <div className={'col-lg-2'}>
                        <button type="button" className="btn btn-primary f-btn" data-bs-toggle="modal"
                                data-bs-target="#Modal2">
                            Price
                        </button>
                    </div>

                    <div className="modal fade" id="Modal2" tabIndex="-1" aria-labelledby="Modal2Label"
                         aria-hidden="true">
                        <div className="modal-dialog">
                            <div className="modal-content">
                                <div className="modal-header">
                                    <h1 className="modal-title fs-5" id="Modal2Label">Price range</h1>
                                    <button type="button" className="btn-close" data-bs-dismiss="modal"
                                            aria-label="Close"></button>
                                </div>
                                <div className="modal-body">
                                    <h5>Min</h5>
                                    <h6>{minPrice}</h6>
                                    <input onChange={event => setMinPrice(event.target.value)} type="range"
                                           className={"form-range"} name="price-min" id="price-min" min={0}
                                           max={1000000} defaultValue={minPrice}/>
                                    <h5>Max</h5>
                                    <h6>{maxPrice}</h6>
                                    <input onChange={event => setMaxPrice(event.target.value)} type="range"
                                           className={"form-range"} name="price-max" id="price-max" min={0}
                                           max={1000000} defaultValue={maxPrice}/>
                                    <h6>Sort order</h6>
                                    <div  className="form-check">
                                        <input onClick={() => setPriceOrder('DESC')} className="form-check-input" type="radio" name="flexRadioDefault"
                                               id="flexRadioDefault1"/>
                                        <label className="form-check-label" htmlFor="flexRadioDefault1">
                                            Descending
                                        </label>
                                    </div>
                                    <div className="form-check">
                                        <input onClick={() => {setPriceOrder('ASC'); console.log(priceOrder)}} className="form-check-input" type="radio" name="flexRadioDefault"
                                               id="flexRadioDefault2" checked/>
                                        <label onClick={() => {setPriceOrder('ASC'); console.log(priceOrder)}} className="form-check-label" htmlFor="flexRadioDefault2">
                                            Ascending
                                        </label>
                                    </div>
                                </div>
                                <div className="modal-footer">
                                    <button onClick={() => {
                                        setUrl(`http://localhost:80/cars/with_price_between/${minPrice}/${maxPrice}/${priceOrder}`);
                                        console.log(url)
                                    }

                                    } type="button" className="btn btn-primary" data-bs-dismiss="modal">Filter
                                    </button>
                                </div>


                            </div>

                        </div>
                    </div>
                    {/*End modal 2*/}

                    <div className={"col-lg-2"}>
                        <button onClick={() => setUrl("http://localhost:80/cars/most_expensive")} type="button"
                                className="btn btn-warning f-btn">
                            Highest value
                        </button>
                    </div>
                    <CarsList cars={cars}/>

                </div>
            </div>
        </div>


    )
}}


export default FiltersComponent