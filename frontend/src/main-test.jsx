import React from 'react'
import ReactDOM from 'react-dom/client'

function TestApp() {
    return <div><h1>TEST - React is working!</h1></div>
}

ReactDOM.createRoot(document.getElementById('root')).render(
    <React.StrictMode>
        <TestApp />
    </React.StrictMode>,
)
