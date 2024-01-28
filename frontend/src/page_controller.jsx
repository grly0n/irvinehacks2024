import React from "react";
import {BrowserRouter, Routes, Route} from "react-router-dom";

import Calendar_page from "./components/pages/calendar_page.jsx";
import Home from "./components/pages/home.jsx";
import Timer_page from "./components/pages/countdown_timer_page.jsx";

export default function Controller(){
    return(
        <>
            <BrowserRouter>
                <Routes>
                    <Route index element = {<Home />} /> 
                    <Route exact path="/home" element = {<Home />} /> 
                    <Route exact path="/calendar" element = {<Calendar_page />} /> 
                    <Route exact path = "/timer" element = {<Timer_page />} />


                </Routes>
            </BrowserRouter>
        </>


    );



}