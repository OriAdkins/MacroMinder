import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const navigate = useNavigate();

  function handleOpenRegisterPage() {
    navigate('/RegisterPage');
  }

  const handleUsernameChange = (value) => {
    const cleanedValue = value.replace(/[^a-zA-Z0-9]/g, "").toLowerCase();
    setUsername(cleanedValue);
  };

  const handlePasswordChange = (value) => {
    setPassword(value);
  };

  /*

  const displayErrorMessage = (message) => {
    alert(message);
  };
  
  const displaySuccessMessage = (message) => {
    alert(message);
  };
  */
  return (
    <div style={styles.container}>
      <h2 style={styles.title}>Log In</h2>
      <input
        style={styles.input}
        placeholder="Username"
        value={username}
        onChange={(e) => handleUsernameChange(e.target.value)}
      />
      <input
        style={styles.input}
        placeholder="Password"
        value={password}
        type="password"
        onChange={(e) => handlePasswordChange(e.target.value)}
      />
      <div style={styles.buttonContainer}>
        <button /*onClick={handleLogin}*/ >Log In</button>
        <button /*onClick={handleOpenHomePage}*/ >Return Home</button>
        <p>No Account?</p>
        <button onClick={handleOpenRegisterPage}>Sign up</button>
        <p>Email not needed*</p>
      </div>
    </div>
  );
}

const styles = {
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  title: {
    fontSize: 24,
    marginBottom: 20,
  },
  input: {
    width: '100%',
    marginBottom: 10,
    padding: 10,
    borderWidth: 1,
    borderColor: 'gray',
    borderRadius: 5,
  },
  buttonContainer: {
    marginTop: 10,
    width: '100%',
  },
};

export default LoginPage;