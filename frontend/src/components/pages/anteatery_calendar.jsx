import './page.css'
import Calendar from "./calendar/calendar_component.jsx";
import Header from "../header.jsx";
export default function Anteatery_calendar_page(){
    const food = ["meatloaf","taco", "breadstick", "meatloaf","meatloaf","meatloaf","meatloaf"];
    return (
        <>
            <Header />
            <h1 style={{color: "beige", backgroundColor:"darkred",marginLeft:224, marginRight:224}}> Anteatery food for the week :)</h1>
            
            <Calendar data={food}/>
            <p className='show_full_page_calendar'> </p>
        </>

    );


}
