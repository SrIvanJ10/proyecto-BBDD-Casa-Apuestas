import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { register, verifyOtp } from '../services/authService';

const Register = () => {
    const [step, setStep] = useState('register'); // 'register' or 'verify'
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: '',
        confirmPassword: ''
    });
    const [otpData, setOtpData] = useState({
        code: '',
        userEmail: '',
        inputOtp: ''
    });
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        if (formData.password !== formData.confirmPassword) {
            setError('Las contraseñas no coinciden');
            return;
        }

        setLoading(true);
        try {
            const response = await register({
                username: formData.username,
                email: formData.email,
                password: formData.password
            });

            // El backend devuelve el OTP code en desarrollo
            if (response.otp_code) {
                setOtpData({
                    code: response.otp_code,
                    userEmail: response.email,
                    inputOtp: ''
                });
                setStep('verify');
            } else {
                // Si por alguna razón no hay OTP, redirigir a login
                navigate('/login');
            }
        } catch (err) {
            const errorMsg = err.response?.data?.error || 'Error al registrarse. Inténtalo de nuevo.';
            setError(errorMsg);
        } finally {
            setLoading(false);
        }
    };

    const handleVerifyOtp = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            const response = await verifyOtp(otpData.userEmail, otpData.inputOtp);

            // Si la verificación es exitosa, el servicio ya guarda el token
            // Redirigir al home ya logueado
            navigate('/');
        } catch (err) {
            const errorMsg = err.response?.data?.error || 'Error al verificar OTP. Inténtalo de nuevo.';
            setError(errorMsg);
        } finally {
            setLoading(false);
        }
    };

    if (step === 'verify') {
        return (
            <div className="container" style={{ paddingTop: '4rem', paddingBottom: '4rem', maxWidth: '500px' }}>
                <div className="card">
                    <h2 style={{ textAlign: 'center', marginBottom: '1rem' }}>✉️ Verifica tu Email</h2>
                    <p style={{ textAlign: 'center', color: 'var(--text-secondary)', marginBottom: '2rem' }}>
                        Se ha enviado un código de verificación a tu email
                    </p>

                    {/* Mostrar el OTP code prominentemente (simulando "revisa tu email") */}
                    <div style={{
                        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                        color: 'white',
                        padding: '2rem',
                        borderRadius: '1rem',
                        textAlign: 'center',
                        marginBottom: '2rem',
                        boxShadow: '0 10px 25px rgba(0,0,0,0.1)'
                    }}>
                        <p style={{ fontSize: '0.9rem', opacity: 0.9, marginBottom: '0.5rem' }}>
                            🔐 Tu código de verificación
                        </p>
                        <p style={{
                            fontSize: '2.5rem',
                            fontWeight: 'bold',
                            letterSpacing: '0.3rem',
                            margin: '0.5rem 0',
                            fontFamily: 'monospace'
                        }}>
                            {otpData.code}
                        </p>
                        <p style={{ fontSize: '0.8rem', opacity: 0.8, marginTop: '0.5rem' }}>
                            (En producción, recibirías esto por email)
                        </p>
                    </div>

                    {error && (
                        <div style={{
                            background: '#fed7d7',
                            color: '#c53030',
                            padding: '1rem',
                            borderRadius: '0.5rem',
                            marginBottom: '1.5rem'
                        }}>
                            {error}
                        </div>
                    )}

                    <form onSubmit={handleVerifyOtp}>
                        <div style={{ marginBottom: '1.5rem' }}>
                            <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '600' }}>
                                Introduce el código de verificación
                            </label>
                            <input
                                type="text"
                                value={otpData.inputOtp}
                                onChange={(e) => setOtpData({ ...otpData, inputOtp: e.target.value })}
                                placeholder="Ejemplo: 123456"
                                style={{
                                    width: '100%',
                                    padding: '0.75rem',
                                    borderRadius: '0.5rem',
                                    border: '1px solid #e2e8f0',
                                    fontSize: '1.1rem',
                                    textAlign: 'center',
                                    letterSpacing: '0.2rem',
                                    fontFamily: 'monospace'
                                }}
                                required
                                autoFocus
                            />
                        </div>

                        <button
                            type="submit"
                            className="btn btn-primary"
                            style={{ width: '100%' }}
                            disabled={loading}
                        >
                            {loading ? 'Verificando...' : 'Verificar y Activar Cuenta'}
                        </button>
                    </form>

                    <p style={{ textAlign: 'center', marginTop: '1.5rem', color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
                        💡 <strong>Modo Desarrollo:</strong> Copia el código de arriba y pégalo en el campo
                    </p>
                </div>
            </div>
        );
    }

    return (
        <div className="container" style={{ paddingTop: '4rem', paddingBottom: '4rem', maxWidth: '500px' }}>
            <div className="card">
                <h2 style={{ textAlign: 'center', marginBottom: '2rem' }}>Crear Cuenta</h2>
                {error && (
                    <div style={{
                        background: '#fed7d7',
                        color: '#c53030',
                        padding: '1rem',
                        borderRadius: '0.5rem',
                        marginBottom: '1.5rem'
                    }}>
                        {error}
                    </div>
                )}
                <form onSubmit={handleSubmit}>
                    <div style={{ marginBottom: '1.5rem' }}>
                        <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '600' }}>Usuario</label>
                        <input
                            type="text"
                            value={formData.username}
                            onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                            style={{ width: '100%', padding: '0.75rem', borderRadius: '0.5rem', border: '1px solid #e2e8f0' }}
                            required
                        />
                    </div>
                    <div style={{ marginBottom: '1.5rem' }}>
                        <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '600' }}>Email</label>
                        <input
                            type="email"
                            value={formData.email}
                            onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                            style={{ width: '100%', padding: '0.75rem', borderRadius: '0.5rem', border: '1px solid #e2e8f0' }}
                            required
                        />
                    </div>
                    <div style={{ marginBottom: '1.5rem' }}>
                        <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '600' }}>Contraseña</label>
                        <input
                            type="password"
                            value={formData.password}
                            onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                            style={{ width: '100%', padding: '0.75rem', borderRadius: '0.5rem', border: '1px solid #e2e8f0' }}
                            required
                        />
                    </div>
                    <div style={{ marginBottom: '1.5rem' }}>
                        <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '600' }}>Confirmar Contraseña</label>
                        <input
                            type="password"
                            value={formData.confirmPassword}
                            onChange={(e) => setFormData({ ...formData, confirmPassword: e.target.value })}
                            style={{ width: '100%', padding: '0.75rem', borderRadius: '0.5rem', border: '1px solid #e2e8f0' }}
                            required
                        />
                    </div>
                    <button
                        type="submit"
                        className="btn btn-primary"
                        style={{ width: '100%' }}
                        disabled={loading}
                    >
                        {loading ? 'Registrando...' : 'Registrarse'}
                    </button>
                </form>
                <p style={{ textAlign: 'center', marginTop: '1.5rem', color: 'var(--text-secondary)' }}>
                    ¿Ya tienes cuenta? <Link to="/login" style={{ color: 'var(--primary)', fontWeight: '600' }}>Inicia Sesión</Link>
                </p>
            </div>
        </div>
    );
};

export default Register;
