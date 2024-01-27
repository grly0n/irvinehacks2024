import React from 'react'
import ReactDOM from 'react-dom/client'
import Controller from './page_controller.jsx'


/* Header doesnt make sense */
ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <Controller />

  </React.StrictMode>,
)
