import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import Advanced3DSolarSystem from '../components/Advanced3DSolarSystem';
import DemoModal from '../components/DemoModal';
import InteractiveStory from '../components/InteractiveStory';
import ExoplanetHunt from '../components/ExoplanetHunt';
import StarExplorer from '../components/StarExplorer';
import './Home.css';

const Home = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [showDemo, setShowDemo] = useState(false);
  const [showStory, setShowStory] = useState(false);
  const [showHunt, setShowHunt] = useState(false);
  const [showExplorer, setShowExplorer] = useState(false);

  // Mission data - could be moved to a separate data file later
  const missionData = [
    {
      id: 1,
      date: 'OCTOBER 5, 2025 AT 11:00 A.M.',
      title: 'New Horizon',
      description: 'Embark on a thrilling adventure to the distant reaches of our galaxy, exploring undiscovered worlds and encountering strange alien civilizations.',
      image: 'https://images.unsplash.com/photo-1446776653964-20c1d3a81b06?w=400&h=300&fit=crop',
      type: 'mission',
      status: 'active'
    },
    {
      id: 2,
      date: 'OCTOBER 4, 2025 AT 3:30 P.M.',
      title: 'Galactic Odyssey',
      description: 'Join a brave team of space explorers on a perilous journey across the galaxy, pushing the boundaries of human knowledge and discovery.',
      image: 'https://images.unsplash.com/photo-1502134249126-9f3755a50d78?w=400&h=300&fit=crop',
      type: 'mission',
      status: 'completed'
    },
    {
      id: 3,
      date: 'OCTOBER 3, 2025 AT 10:00 A.M.',
      title: 'Cosmic Quest',
      description: 'Enter a new realm of space exploration and adventure, as you journey through uncharted galaxies, encountering strange and wondrous sights along the way.',
      image: 'https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?w=400&h=300&fit=crop',
      type: 'mission',
      status: 'upcoming'
    },
    {
      id: 4,
      date: 'OCTOBER 1, 2025 AT 11:00 A.M.',
      title: 'Stellar Bound',
      description: 'Join a team of brave space explorers on a perilous journey through the cosmos, encountering mysterious phenomena and ancient secrets.',
      image: 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400&h=300&fit=crop',
      type: 'mission',
      status: 'completed'
    }
  ];

  // Filter missions based on search term
  const filteredMissions = missionData.filter(mission => {
    const searchLower = searchTerm.toLowerCase();
    return mission.title.toLowerCase().includes(searchLower) ||
           mission.description.toLowerCase().includes(searchLower);
  });

  return (
    <div className="home page-container">
      <div className="home-header">
        <h1 className="page-title">Nexa - AI Exoplanet Discovery</h1>
        <button className="demo-btn" onClick={() => setShowDemo(true)}>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
            <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="2"/>
            <polygon points="10,8 16,12 10,16" fill="currentColor"/>
          </svg>
        </button>
      </div>

      {/* AI Model Prediction Section */}
      <div className="featured-ai-section">
        <div className="ai-hero">
          <div className="ai-hero-content">
            <div className="ai-badge">🤖 AI-Powered Detection</div>
            <h2>Discover Exoplanets with Machine Learning</h2>
            <p>Use our advanced ensemble AI model (CatBoost + TabNet) to classify exoplanet candidates. Get instant predictions with SHAP interpretability and chat with Gemini AI for detailed explanations.</p>

            <div className="ai-features">
              <div className="feature-tag">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M9 11H7v2h2v-2zm4 0h-2v2h2v-2zm4 0h-2v2h2v-2zm2-7h-1V2h-2v2H8V2H6v2H5c-1.11 0-1.99.9-1.99 2L3 20c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 16H5V9h14v11z"/>
                </svg>
                95%+ Accuracy
              </div>
              <div className="feature-tag">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                </svg>
                SHAP Explainability
              </div>
              <div className="feature-tag">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M20 2H4c-1.1 0-1.99.9-1.99 2L2 22l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zM6 9h12v2H6V9zm8 5H6v-2h8v2zm4-6H6V6h12v2z"/>
                </svg>
                Gemini AI Chat
              </div>
            </div>

            <div className="ai-cta-buttons">
              <Link to="/explorer" className="ai-cta-btn primary">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                  <path d="M13 3L4 14h7l-1 7 9-11h-7l1-7z" fill="currentColor"/>
                </svg>
                Launch AI Model
              </Link>
              <Link to="/simulator" className="ai-cta-btn secondary">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                  <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="2"/>
                  <path d="M12 6v6l4 2" stroke="currentColor" strokeWidth="2"/>
                </svg>
                View Demo
              </Link>
            </div>
          </div>

          <div className="ai-hero-visual">
            <div className="ai-model-preview">
              <div className="model-card">
                <div className="model-header">
                  <span className="model-label">Input Parameters</span>
                  <span className="model-count">13 Features</span>
                </div>
                <div className="model-features">
                  <div className="feature-item">Period • Duration • Depth</div>
                  <div className="feature-item">Radius • Temperature • Flux</div>
                  <div className="feature-item">Stellar Properties • Coordinates</div>
                </div>
              </div>

              <div className="model-arrow">↓</div>

              <div className="model-card ensemble">
                <div className="model-header">
                  <span className="model-label">Ensemble Model</span>
                  <span className="model-count">2 Algorithms</span>
                </div>
                <div className="model-features">
                  <div className="feature-item gradient">CatBoost Classifier</div>
                  <div className="feature-item gradient">TabNet Neural Network</div>
                </div>
              </div>

              <div className="model-arrow">↓</div>

              <div className="model-card result">
                <div className="model-header">
                  <span className="model-label">Classification Result</span>
                  <span className="model-count">3 Classes</span>
                </div>
                <div className="model-features">
                  <div className="feature-item success">Planet ✓</div>
                  <div className="feature-item warning">Candidate</div>
                  <div className="feature-item error">False Positive</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="ai-stats">
          <div className="stat-item">
            <div className="stat-number">2,662</div>
            <div className="stat-label">Kepler Planets</div>
          </div>
          <div className="stat-item">
            <div className="stat-number">5,000+</div>
            <div className="stat-label">TESS Candidates</div>
          </div>
          <div className="stat-item">
            <div className="stat-number">95%</div>
            <div className="stat-label">Model Accuracy</div>
          </div>
          <div className="stat-item">
            <div className="stat-number">Real-time</div>
            <div className="stat-label">AI Predictions</div>
          </div>
        </div>
      </div>

      <div className="search-section">
        <div className="search-bar">
          <svg className="search-icon" width="20" height="20" viewBox="0 0 24 24" fill="none">
            <circle cx="11" cy="11" r="8" stroke="currentColor" strokeWidth="2"/>
            <path d="m21 21-4.35-4.35" stroke="currentColor" strokeWidth="2"/>
          </svg>
          <input
            type="text"
            placeholder="Search"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="search-input"
          />
        </div>
      </div>

      <div className="missions-section">
        {filteredMissions.length > 0 ? (
          filteredMissions.map((mission) => (
            <Link key={mission.id} to="/explorer" className="mission-card">
              <div className="mission-image">
                <img src={mission.image} alt={mission.title} />
                <div className="mission-overlay"></div>
              </div>
              <div className="mission-content">
                <div className="mission-date">{mission.date}</div>
                <h3 className="mission-title">{mission.title}</h3>
                <p className="mission-description">{mission.description}</p>
              </div>
              <div className="mission-arrow">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                  <path d="M9 18L15 12L9 6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              </div>
            </Link>
          ))
        ) : (
          <div className="no-missions">
            <p>No missions found matching your search.</p>
          </div>
        )}
      </div>

      <div className="solar-system-section">
        <h3>Interactive 3D Solar System</h3>
        <Advanced3DSolarSystem />
        <p className="system-description">
          Explore a fully interactive 3D solar system with realistic planetary orbits, moons, and ring systems. Drag to rotate the view and watch planets move in real-time with accurate orbital mechanics.
        </p>
      </div>

      <div className="interactive-experiences">
        <h3>🚀 Interactive Experiences</h3>
        <div className="experience-grid">
          <div className="experience-card" onClick={() => setShowStory(true)}>
            <div className="experience-icon">📖</div>
            <h4>Discovery Journey</h4>
            <p>Experience the thrilling story of discovering your first exoplanet through interactive storytelling</p>
            <div className="experience-badge">Interactive Story</div>
          </div>
          
          <div className="experience-card" onClick={() => setShowHunt(true)}>
            <div className="experience-icon">🎯</div>
            <h4>Exoplanet Hunt</h4>
            <p>Test your skills in this gamified challenge to detect exoplanets using the transit method</p>
            <div className="experience-badge">Mini Game</div>
          </div>
          
          <div className="experience-card" onClick={() => setShowExplorer(true)}>
            <div className="experience-icon">🗺️</div>
            <h4>Star Explorer</h4>
            <p>Navigate an interactive star map and explore real exoplanetary systems in 3D</p>
            <div className="experience-badge">3D Explorer</div>
          </div>
        </div>
      </div>

      <div className="quick-actions">
        <Link to="/catalog" className="action-card">
          <div className="action-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
              <circle cx="12" cy="12" r="8" stroke="currentColor" strokeWidth="2"/>
              <circle cx="8" cy="8" r="2" fill="currentColor"/>
              <circle cx="16" cy="8" r="1.5" fill="currentColor"/>
              <circle cx="12" cy="16" r="1" fill="currentColor"/>
            </svg>
          </div>
          <span>Exoplanet Catalog</span>
        </Link>
        
        <Link to="/simulator" className="action-card">
          <div className="action-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
              <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="2"/>
              <circle cx="12" cy="12" r="6" fill="currentColor" opacity="0.3"/>
              <circle cx="12" cy="12" r="2" fill="currentColor"/>
            </svg>
          </div>
          <span>Transit Simulator</span>
        </Link>
        
        <Link to="/discovery" className="action-card">
          <div className="action-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
              <path d="M12 2L15.09 8.26L22 9L17 14L18.18 21L12 17.77L5.82 21L7 14L2 9L8.91 8.26L12 2Z" fill="currentColor"/>
            </svg>
          </div>
          <span>Discovery Cards</span>
        </Link>
      </div>

      <DemoModal 
        isOpen={showDemo} 
        onClose={() => setShowDemo(false)} 
      />
      
      <InteractiveStory 
        isOpen={showStory} 
        onClose={() => setShowStory(false)} 
      />
      
      <ExoplanetHunt 
        isOpen={showHunt} 
        onClose={() => setShowHunt(false)} 
      />
      
      <StarExplorer 
        isOpen={showExplorer} 
        onClose={() => setShowExplorer(false)} 
      />
    </div>
  );
};

export default Home;
