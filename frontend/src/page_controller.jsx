import React from "react";
import {BrowserRouter, Routes, Route} from "react-router-dom";

import Anteatery_calendar_page from "./components/pages/anteatery_calendar.jsx";
import Brandywine_calendar_page from "./components/pages/brandywine_calendar.jsx";
import Home from "./components/pages/home.jsx";
import Timer_page from "./components/pages/countdown_timer_page.jsx";

export default function Controller(){
    return(
        <>
            <BrowserRouter>
                <Routes>
                    <Route index element = {<Home />} /> 
                    <Route exact path="/home" element = {<Home />} /> 
                    <Route exact path="/calendar" element = {<Anteatery_calendar_page />} /> 
                    <Route exact path="/calendar/anteatery" element = {<Anteatery_calendar_page />} />
                    <Route exact path="/calendar/brandywine" element = {<Brandywine_calendar_page />} />  
                    <Route exact path = "/timer" element = {<Timer_page />} />
                    <Route path="*" element = {<Home />}></Route>


                </Routes>
            </BrowserRouter>
        </>


    );



}