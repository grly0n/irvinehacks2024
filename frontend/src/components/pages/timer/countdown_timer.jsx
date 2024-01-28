import "./countdown_timer.css"
import { useEffect, useState } from "react";
import date from '../../../../../backend/database/meatloaf_day.txt'
const Timer = () => {
    const [miliseconds,setMiliseconds] = useState(0);
    const [seconds,setSeconds] = useState(0);
    const [minutes,setMinutes] = useState(0);
    const [hours, setHours] = useState(0);
    const [days,setDays] = useState(0);

    let deadline='12/31/24'
    /* Did not implement, find text
    fetch(date)
        .then(d => d.text())
        .then(text => { 
        if (text != 'False'){
            deadline = text;
        }
        else{
            let todays_date= new Date();
            deadline = todays_date.getMonth()+'/'+todays_date.getDate()+ '/'+todays_date.getFullYear();
        }
        });
    console.log({deadline})
    */
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
            
            <p>{days==0&&hours==0&&minutes==0&&seconds==0&&miliseconds==0? 'This sucks, no Meatloaf':'' }</p>
        </>

    );

}
export default Timer