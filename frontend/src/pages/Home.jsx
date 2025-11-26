import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import MatchCard from '../components/MatchCard';
import { getUpcomingMatches, getLiveMatches } from '../services/matchService';

const Home = () => {
  const [upcomingMatches, setUpcomingMatches] = useState([]);
  const [liveMatches, setLiveMatches] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [upcoming, live] = await Promise.all([
          getUpcomingMatches(),
          getLiveMatches()
        ]);
        setUpcomingMatches(upcoming);
        setLiveMatches(live);
      } catch (error) {
        console.error("Error fetching matches:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return <div className="container" style={{ padding: '4rem', textAlign: 'center' }}>Cargando...</div>;
  }

  return (
    <main>
      <section className="hero" style={{
        background: 'linear-gradient(135deg, var(--secondary) 0%, var(--secondary-dark) 100%)',
        color: 'white',
        padding: '6rem 0',
        textAlign: 'center'
      }}>
        <div className="container">
          <h1 style={{ fontSize: '3.5rem', marginBottom: '1.5rem', color: 'white' }}>
            Vive la emoción del deporte
          </h1>
          <p style={{ fontSize: '1.25rem', marginBottom: '2.5rem', opacity: 0.9, maxWidth: '600px', margin: '0 auto 2.5rem' }}>
            La mejor plataforma de apuestas deportivas con predicciones impulsadas por Inteligencia Artificial.
          </p>
          <Link to="/matches" className="btn btn-primary" style={{ fontSize: '1.1rem', padding: '1rem 2rem' }}>
            Ver Partidos
          </Link>
        </div>
      </section>

      {liveMatches.length > 0 && (
        <section className="section" style={{ padding: '4rem 0', background: '#fff5f5' }}>
          <div className="container">
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '2rem', justifyContent: 'center' }}>
              <span style={{ width: '12px', height: '12px', background: '#e53e3e', borderRadius: '50%', display: 'inline-block', animation: 'pulse 1.5s infinite' }}></span>
              <h2 className="text-gradient" style={{ margin: 0 }}>En Vivo Ahora</h2>
            </div>
            <div className="matches-grid" style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
              gap: '2rem'
            }}>
              {liveMatches.map(match => (
                <MatchCard key={match.id} match={match} live={true} />
              ))}
            </div>
          </div>
        </section>
      )}

      <section className="section" style={{ padding: '4rem 0' }}>
        <div className="container">
          <h2 className="text-gradient" style={{ textAlign: 'center', marginBottom: '3rem' }}>
            Próximos Partidos
          </h2>
          {upcomingMatches.length > 0 ? (
            <div className="matches-grid" style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
              gap: '2rem'
            }}>
              {upcomingMatches.map(match => (
                <MatchCard key={match.id} match={match} />
              ))}
            </div>
          ) : (
            <p style={{ textAlign: 'center', color: 'var(--text-secondary)' }}>No hay partidos próximos programados.</p>
          )}
        </div>
      </section>

      <style>{`
                @keyframes pulse {
                    0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(229, 62, 62, 0.7); }
                    70% { transform: scale(1); box-shadow: 0 0 0 10px rgba(229, 62, 62, 0); }
                    100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(229, 62, 62, 0); }
                }
            `}</style>
    </main>
  );
};

export default Home;