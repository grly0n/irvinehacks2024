import Header from "../header.jsx"; 
import Button from "./timer/congrats_button.jsx";
import Timer from "./timer/countdown_timer.jsx";
export default function Timer_page(){
    return(
        <>
            <Header />
            <h1> GET HYPED FOR MEATLOAF!!!</h1>
            <Timer />
            <p> </p>
            <Button />
        </>
    );


}