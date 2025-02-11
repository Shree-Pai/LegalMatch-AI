import React, { useState, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faSearch, faExclamationTriangle, faMoon, faSun,
  faStar, faGavel, faUniversity, faMapMarkerAlt, faDollarSign, faHandHoldingHeart
} from '@fortawesome/free-solid-svg-icons';
import './App.css';

function App() {
  const [case_type, setCaseType] = useState('');
  const [description, setDescription] = useState('');
  const [recommendations, setRecommendations] = useState([]);
  const [error, setError] = useState('');
  const [formErrors, setFormErrors] = useState({});
  const [darkMode, setDarkMode] = useState(
    localStorage.getItem('darkMode') === 'true' // Load theme from local storage
  );

  useEffect(() => {
    document.body.className = darkMode ? 'dark-mode' : 'light-mode';
    localStorage.setItem('darkMode', darkMode); // Save theme preference
  }, [darkMode]);

  const LawyerCard = ({ lawyer }) => (
    <div className="lawyer-card">
      <div className="lawyer-header">
        <div>
          <h3 className="lawyer-name">{lawyer.name}</h3>
          <p className="lawyer-specialization">{lawyer.specialization}</p>
        </div>
        <div className="rating">
          <FontAwesomeIcon icon={faStar} />
          <span>{lawyer.feedback_score.toFixed(1)}/5.0</span>
        </div>
      </div>

      <div className="lawyer-details">
        <div className="detail-item">
          <FontAwesomeIcon icon={faGavel} />
          <span>{lawyer.experience_years} years experience</span>
        </div>
        <div className="detail-item">
          <FontAwesomeIcon icon={faUniversity} />
          <span>{lawyer.law_school}</span>
        </div>
        <div className="detail-item">
          <FontAwesomeIcon icon={faMapMarkerAlt} />
          <span>{lawyer.location}</span>
        </div>
        <div className="detail-item">
          <FontAwesomeIcon icon={faDollarSign} />
          <span>${lawyer.hourly_rate}/hr</span>
        </div>
      </div>

      <div className="lawyer-stats">
        <div className="stat-item">
          <span>Success Rate:</span>
          <span className="success-rate">{(lawyer.success_rate * 100).toFixed(1)}%</span>
        </div>
        <div className="stat-item">
          <span>Recent Cases:</span>
          <span>{lawyer.recent_cases}</span>
        </div>
        <div className="stat-item">
          <FontAwesomeIcon icon={faHandHoldingHeart} />
          <span>Pro Bono Cases: {lawyer.pro_bono_cases}</span>
        </div>
      </div>
      <div className="lawyer-description">
        <h4>About {lawyer.name}</h4>
        <p>{lawyer.description}</p>
      </div>
    </div>
  );

  const isFormValid = case_type.trim() !== '' && description.trim() !== '';

  const validateForm = () => {
    let errors = {};
    if (!case_type.trim()) errors.case_type = 'Case Type is required.';
    if (!description.trim()) errors.description = 'Case Description is required.';
    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleRecommendLawyers = async () => {
    setError('');
    if (!validateForm()) return;
    try {
      const response = await fetch('http://localhost:5000/recommend_lawyers', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ case_type, description }),
      });
      const data = await response.json();
      if (response.ok) {
        setRecommendations(data.recommendations);
      } else {
        setError(data.message || 'An error occurred while fetching recommendations.');
      }
    } catch (err) {
      setError('An error occurred while fetching recommendations.');
    }
  };

  return (
    <div className={`app-container ${darkMode ? 'dark' : 'light'}`}>
      {/* Navbar */}
      <nav className="navbar">
        <h1 className="logo">
          ⚖️LegalMatch AI
        </h1>
        <button className="theme-toggle" onClick={() => setDarkMode(!darkMode)}>
          <FontAwesomeIcon icon={darkMode ? faSun : faMoon} />
        </button>
      </nav>

      {/* Main content */}
      <div className="container">
        <div className="input-group">
          <label>Case Type</label>
          <select
            value={case_type}
            onChange={(e) => setCaseType(e.target.value)}
            className="case-type-dropdown"
          >
            <option value="">Select a case type</option>
            <option value="Tax Law">Tax Law</option>
            <option value="Criminal">Criminal</option>
            <option value="Corporate">Corporate</option>
            <option value="Family">Family</option>
            <option value="Civil">Civil</option>
            <option value="Intellectual Property">Intellectual Property</option>
          </select>
          {formErrors.caseType && <p className="validation-error">{formErrors.caseType}</p>}
        </div>

        <div className="input-group">
          <label>Case Description</label>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Describe your case"
          />
          {formErrors.description && <p className="validation-error">{formErrors.description}</p>}
        </div>

        <div className="buttons">
          <button
            className="btn recommend"
            onClick={handleRecommendLawyers}
            disabled={!isFormValid || Object.keys(formErrors).length > 0}
          >
            <FontAwesomeIcon icon={faSearch} /> Recommend Lawyers
          </button>
        </div>

        {error && (
          <p className="error">
            <FontAwesomeIcon icon={faExclamationTriangle} /> {error}
          </p>
        )}

        {recommendations.length > 0 && (
          <div className="result">
            <h2>Recommended Lawyers</h2>
            <div className="lawyer-cards-grid">
              {recommendations.map((lawyer) => (
                <LawyerCard key={lawyer.lawyer_id} lawyer={lawyer} />
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
