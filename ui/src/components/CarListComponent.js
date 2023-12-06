import React from "react";
import './stylesheets/CarListComponent.css'
const CarListComponent = ({car}) => {
    return (
        <div className={"row car-component"}>
            <div className={"col-3"}>
                <img src={`${car.icon}`}/>
            </div>
            <div className={"col-9"}>
                <div className={"row"} >
                    <div className={"col-10"}>
                        <div className={"row"}>
                            <div className={"col-12"}>
                                <p className={"fs-5"}>{car.model}</p>
                            </div>
                            <div className={"col-12"}>
                                <p>{car.mileage} km</p>
                            </div>
                            <div className={"col-12"}>
                                <p>{car.components.map(c => `${c.name} `)}</p>
                            </div>
                            <div className={"col-12"}>
                                <div className={"color-div"} style={{background: `${car.color}`}}></div>
                            </div>
                        </div>

                    </div>

                    <div className={"col-2"}>
                        <h5>{car.price} PLN</h5>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default CarListComponent