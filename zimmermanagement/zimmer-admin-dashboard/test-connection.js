// Simple test to check backend connection
fetch('http://localhost:8000/health')
  .then(response => response.json())
  .then(data => {
    console.log('✅ Backend connection successful:', data);
  })
  .catch(error => {
    console.error('❌ Backend connection failed:', error);
  });

// Test login
fetch('http://localhost:8000/api/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    email: 'admin@zimmer.com',
    password: 'admin123'
  })
})
.then(response => response.json())
.then(data => {
  console.log('✅ Login successful:', data);
  
  // Test KB status with token
  if (data.access_token) {
    fetch('http://localhost:8000/api/admin/kb-status', {
      headers: {
        'Authorization': `Bearer ${data.access_token}`,
        'Content-Type': 'application/json',
      }
    })
    .then(response => response.json())
    .then(kbData => {
      console.log('✅ KB Status API successful:', kbData);
    })
    .catch(error => {
      console.error('❌ KB Status API failed:', error);
    });
  }
})
.catch(error => {
  console.error('❌ Login failed:', error);
}); 