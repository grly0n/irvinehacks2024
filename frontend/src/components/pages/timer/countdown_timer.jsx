import "./countdown_timer.css"
import { useEffect, useState } from "react";
const Timer = () => {
    const [miliseconds,setMiliseconds] = useState(0);
    const [seconds,setSeconds] = useState(0);
    const [minutes,setMinutes] = useState(0);
    const [hours, setHours] = useState(0);
    const [days,setDays] = useState(0);


    let deadline = "December 31, 2024";

    const time_diff=()=>{
        
        const time= Date.parse(deadline)- Date.now();
        
        setMiliseconds(time%1000);
        setSeconds(Math.floor((time/(1000))%60));
        setMinutes(Math.floor((time/(1000*60))%60));
        setHours(Math.floor((time/(1000*60*60))%24))
        setDays(Math.floor((time/(1000*60*60*24))));

        

    }
    useEffect (() =>{
        const interval = setInterval(()=> {
            time_diff()
        },1);
        return () => clearInterval(interval);


    }, []);

    return (

        <>
            <table className='meatloafTimer'>
                <tr>
                    <th>
                        Days
                    </th>
                    <th>
                        Hours
                    </th>
                    <th>
                        Minutes
                    </th>
                    <th>
                        Seconds
                    </th>
                    <th>
                        Milliseconds
                    </th>
                </tr>
                <tr>
                    <th>
                        {days}
                    </th>
                    <th>
                        {hours}
                    </th>
                    <th>
                        {minutes}
                    </th>
                    <th>
                        {seconds}
                    </th>
                    <th>
                        {miliseconds}
                    </th>

                </tr>

            </table>
            
        
        </>

    );

}
export default Timer