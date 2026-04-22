// Platform selection
const platformElements = document.querySelectorAll('.platform');
const selectedPlatforms = new Set();
const maxPlatforms = 2;

platformElements.forEach(platform => {
  platform.addEventListener('click', function() {
    const value = this.getAttribute('data-value');
    
    if (this.classList.contains('active')) {
      // Deselect if already active
      this.classList.remove('active');
      selectedPlatforms.delete(value);
    } else {
      // Select if under limit
      if (selectedPlatforms.size < maxPlatforms) {
        this.classList.add('active');
        selectedPlatforms.add(value);
      } else {
        // Show feedback that limit is reached
        showFeedback(`Please select only ${maxPlatforms} platforms`);
      }
    }
    
    updateSelectionFeedback();
  });
});

function updateSelectionFeedback() {
  const feedback = document.getElementById('platformSelectionFeedback');
  if (selectedPlatforms.size === 0) {
    feedback.textContent = '';
  } else if (selectedPlatforms.size === 1) {
    feedback.textContent = `${selectedPlatforms.size} platform selected. Pick ${maxPlatforms - selectedPlatforms.size} more.`;
  } else if (selectedPlatforms.size === maxPlatforms) {
    feedback.textContent = `✓ ${maxPlatforms} platforms selected`;
  }
}

function showFeedback(message) {
  const feedback = document.getElementById('platformSelectionFeedback');
  feedback.textContent = message;
  setTimeout(() => {
    updateSelectionFeedback();
  }, 2000);
}

// Login button
document.getElementById('login').addEventListener('click', function() {
  const email = document.getElementById('email').value.trim();
  const statusEl = document.getElementById('loginStatus');
  
  if (!email) {
    statusEl.textContent = 'Please enter an email';
    statusEl.style.color = '#ff7a18';
    return;
  }
  
  if (!email.includes('@')) {
    statusEl.textContent = 'Please enter a valid email';
    statusEl.style.color = '#ff7a18';
    return;
  }
  
  statusEl.textContent = '✓ Logged in';
  statusEl.style.color = '#4CAF50';
});

// Analyze button
document.getElementById('start').addEventListener('click', function() {
  const email = document.getElementById('email').value.trim();
  const username = document.getElementById('username').value.trim();
  const consent = document.getElementById('consent').checked;
  
  if (!email) {
    alert('Please enter your email');
    return;
  }
  
  if (!username) {
    alert('Please enter your username');
    return;
  }
  
  if (selectedPlatforms.size !== maxPlatforms) {
    alert(`Please select exactly ${maxPlatforms} platforms`);
    return;
  }
  
  if (!consent) {
    alert('Please agree to data usage');
    return;
  }
  
  // Send data to backend
  const payload = {
    email: email,
    username: username,
    platforms: Array.from(selectedPlatforms)
  };
  
  console.log('Sending payload:', payload);
  
  // Send to backend API
  fetch('http://127.0.0.1:8000/analyze', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(payload)
  })
  .then(response => response.json())
  .then(data => {
    console.log('Success:', data);
    
    // Store analysis ID and email for dashboard
    if (data.analysis_id) {
      localStorage.setItem('currentAnalysisId', data.analysis_id);
    }
    localStorage.setItem('userEmail', email);
    
    // Open dashboard
    const dashboardPath = chrome.runtime.getURL('../../Dashboard/dashboard.html');
    window.open(dashboardPath + `?email=${encodeURIComponent(email)}`, '_blank');
    alert('Analysis started! Dashboard is opening...');
  })
  .catch(error => {
    console.error('Error:', error);
    alert('Error starting analysis. Please try again.');
  });
});
