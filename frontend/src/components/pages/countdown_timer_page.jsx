import './page.css'
import Header from "../header.jsx"; 
import Button from "./timer/congrats_button.jsx";
import Timer from "./timer/countdown_timer.jsx";
export default function Timer_page(){
    return(
        <>
            <Header />
            <h1 style={{color: "beige", backgroundColor:"darkred",marginLeft:224, marginRight:224}}> GET HYPED FOR MEATLOAF!!!</h1>
            <Timer />
            <p> </p>
            <Button />
            <p className=' show_full_page_countdown'> </p>
        </>
    );


}