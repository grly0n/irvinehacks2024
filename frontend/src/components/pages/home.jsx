import './page.css'
import React from 'react';
import Header from '../header';

export default function Home() {
    
    return (
        <>
            
            <Header />
            <h1 style={{color: "beige", backgroundColor:"darkred", marginLeft:224, marginRight:224}}>Welcome to the Brandeatery!</h1>
            <p style={{color: "beige", backgroundColor:"darkred",marginLeft:224, marginRight:224}}> We take the data from the UCI dining halls (Brandywine and the Anteatery) and plan them nicely on a calander.</p>
            <p style={{color: "beige", backgroundColor:"darkred",marginLeft:224, marginRight:224}}> Along the way, we hope to meat expectations: don't expect any loafing around!</p>
            <img src="../../../public/Brandeatery Logo.png" width='500' length='300'></img>
            <p className=' show_full_page_home'> </p>
            
        </>
    );


}