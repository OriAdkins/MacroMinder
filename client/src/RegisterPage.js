import React from 'react';

function RegisterPage(){
    return(
    <div style={styles.container}>
      <h2 style={styles.title}>RegisterPage</h2>
    </div>
    );
}

const styles = {
    container: {
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
      alignItems: 'center',
      padding: 20,
    },
    title: {
      fontSize: 24,
      marginBottom: 20,
    },
  };

export default RegisterPage;