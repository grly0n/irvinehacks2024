import './page.css'
import Calendar from "./calendar/calendar_component.jsx";
import Header from "../header.jsx";
export default function Brandywine_calendar_page(){
    const food = ["meatloaf","taco", "breadstick", "meatloaf","chinese","meatloaf","meatloaf"];
    return (
        <>
            <Header />
            <h1 style={{color: "beige", backgroundColor:"darkred",marginLeft:224, marginRight:224}}> Brandywine food for the week :)</h1>
            <Calendar data={food}/>
            <p className='show_full_page_calendar'> </p>
        </>

    );


}
