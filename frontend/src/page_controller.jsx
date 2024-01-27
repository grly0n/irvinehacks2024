import React from "react";
import {BrowserRouter, Routes, Route} from "react-router-dom";

import Calendar_page from "./components/pages/calendar_page.jsx";
import Home from "./components/pages/home.jsx";

export default function Controller(){
    return(
        <>
            <BrowserRouter>
                <Routes>
                    <Route index element = {<Home />} /> 
                    <Route exact path="/home" element = {<Home />} /> 
                    <Route exact path="/Calendar" element = {<Calendar_page />} /> 


                </Routes>
            </BrowserRouter>
        </>


    );



}