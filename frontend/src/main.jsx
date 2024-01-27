import React from 'react'
import ReactDOM from 'react-dom/client'
import Calender from './components/pages/calendar/calendar_component.jsx'
import Header from './components/headerlinks.jsx'


/* Header doesnt make sense */
ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <Header />
    <Calender />
  </React.StrictMode>,
)
