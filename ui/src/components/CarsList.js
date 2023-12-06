import React from "react"
import CarListComponent from "./CarListComponent";

const CarsList = ({cars}) => {
    if (!cars) {
        cars = []
    }

    return (
        <div className={"container"}>
            <h3>Available cars</h3>
            <p>Found: <strong>{cars.length}</strong></p>
            {
                cars && cars.map(car => <CarListComponent car={car}/>)
            }
        </div>
    )
}


export default CarsList