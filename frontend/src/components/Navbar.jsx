import React, { useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import './Navbar.css'; // We'll create this specific CSS or use global classes

const Navbar = () => {
  const { user, logout } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <header className="header">
      <div className="container">
        <Link to="/" className="logo">
          Sport<span>365</span>
        </Link>
        <nav className="nav">
          <Link to="/">Inicio</Link>
          <Link to="/matches">Partidos</Link>
          <Link to="/leaderboard">Ranking</Link>
          {user && <Link to="/recommendations">Recomendaciones</Link>}
          {user && <Link to="/friends">Amigos</Link>}
          {user && user.is_staff && <Link to="/admin" style={{ color: '#f59e0b', fontWeight: 'bold' }}>⚙️ Admin</Link>}
        </nav>
        <div className="user-actions">
          {user ? (
            <>
              <Link to="/profile" className="btn btn-secondary" style={{ borderColor: 'transparent' }}>
                {user.username || 'Perfil'}
              </Link>
              <button onClick={handleLogout} className="btn btn-primary">
                Salir
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="btn btn-secondary">
                Iniciar Sesión
              </Link>
              <Link to="/register" className="btn btn-primary">
                Registrarse
              </Link>
            </>
          )}
        </div>
      </div>
    </header>
  );
};

export default Navbar;