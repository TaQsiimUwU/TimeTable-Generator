import { useState, useEffect } from 'react'
import './CSS/index.css'

function App() {
  const [activeTab, setActiveTab] = useState<string>('health');
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const API_BASE_URL = 'http://127.0.0.1:3000/api';

  const fetchData = async (endpoint: string) => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`);
      const result = await response.json();

      if (!response.ok) {
        throw new Error(result.error || `HTTP error! status: ${response.status}`);
      }

      setData(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
      setData(null);
    } finally {
      setLoading(false);
    }
  };

  const handleTabClick = (tab: string, endpoint: string) => {
    setActiveTab(tab);
    fetchData(endpoint);
  };

  useEffect(() => {
    // Load health check on component mount
    fetchData('/health');
  }, []);

  const renderTable = (items: any[], title: string) => {
    if (!items || items.length === 0) {
      return <p className="no-data">No {title.toLowerCase()} found.</p>;
    }

    const headers = Object.keys(items[0]);

    return (
      <div className="table-container">
        <h3>{title} ({items.length} items)</h3>
        <table className="data-table">
          <thead>
            <tr>
              {headers.map(header => (
                <th key={header}>{header.replace(/_/g, ' ').toUpperCase()}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {items.map((item, index) => (
              <tr key={index}>
                {headers.map(header => (
                  <td key={header}>{item[header] || 'N/A'}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  };

  const renderContent = () => {
    if (loading) {
      return <div className="loading">Loading...</div>;
    }

    if (error) {
      return (
        <div className="error">
          <h3>Error</h3>
          <p>{error}</p>
          <button onClick={() => fetchData('/health')}>Retry</button>
        </div>
      );
    }

    if (!data) {
      return <div className="no-data">No data available</div>;
    }

    // Handle health check response
    if (activeTab === 'health') {
      return (
        <div className="health-status">
          <h3>Health Check</h3>
          <div className="status-info">
            <p><strong>Status:</strong> <span className={`status ${data.status}`}>{data.status}</span></p>
            {data.database && <p><strong>Database:</strong> {data.database}</p>}
            {data.message && <p><strong>Message:</strong> {data.message}</p>}
            {data.stats && (
              <div className="stats">
                <h4>Database Statistics:</h4>
                <ul>
                  {Object.entries(data.stats).map(([key, value]) => (
                    <li key={key}><strong>{key}:</strong> {value as string}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>
      );
    }

    // Handle API responses with data array
    if (data.success && data.data) {
      if (Array.isArray(data.data)) {
        return renderTable(data.data, activeTab);
      } else {
        // Single item response
        return (
          <div className="single-item">
            <h3>{activeTab} Details</h3>
            <div className="item-details">
              {Object.entries(data.data).map(([key, value]) => (
                <p key={key}><strong>{key.replace(/_/g, ' ')}:</strong> {value as string}</p>
              ))}
            </div>
          </div>
        );
      }
    }

    return <pre className="json-display">{JSON.stringify(data, null, 2)}</pre>;
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>🎓 TimeTable Generator Dashboard</h1>
        <p>Manage courses, instructors, rooms, and timeslots</p>
      </header>

      <nav className="nav-tabs">
        <button
          className={activeTab === 'health' ? 'active' : ''}
          onClick={() => handleTabClick('health', '/health')}
        >
          🔋 Health Check
        </button>
        <button
          className={activeTab === 'courses' ? 'active' : ''}
          onClick={() => handleTabClick('courses', '/courses')}
        >
          📚 Courses
        </button>
        <button
          className={activeTab === 'instructors' ? 'active' : ''}
          onClick={() => handleTabClick('instructors', '/instructors')}
        >
          👨‍🏫 Instructors
        </button>
        <button
          className={activeTab === 'rooms' ? 'active' : ''}
          onClick={() => handleTabClick('rooms', '/rooms')}
        >
          🏢 Rooms
        </button>
        <button
          className={activeTab === 'timeslots' ? 'active' : ''}
          onClick={() => handleTabClick('timeslots', '/timeslots')}
        >
          ⏰ Timeslots
        </button>
        <button
          className={activeTab === 'stats' ? 'active' : ''}
          onClick={() => handleTabClick('stats', '/stats')}
        >
          📊 Statistics
        </button>
      </nav>

      <main className="main-content">
        {renderContent()}
      </main>

      <footer className="app-footer">
        <p>Current endpoint: <code>{API_BASE_URL}/{activeTab}</code></p>
      </footer>
    </div>
  )
}

export default App
