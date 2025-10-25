import React, { useState, useEffect } from 'react'
import axios from 'axios'

const Home = () => {
  const [message, setMessage] = useState('Cargando...')

  useEffect(() => {
    // Test connection to Django backend
    axios.get('/api/test/')
      .then(response => {
        setMessage(response.data.message)
      })
      .catch(error => {
        setMessage('Error conectando con el backend')
        console.error('Error:', error)
      })
  }, [])

  return (
    <div>
      <h1>SportPredict - React Frontend</h1>
      <p>Estado del backend: {message}</p>
    </div>
  )
}

export default Home