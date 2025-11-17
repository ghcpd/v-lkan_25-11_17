import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './index.css';
import ZodiacCard from './components/ZodiacCard';
import ZodiacModal from './components/ZodiacModal';
import SearchBar from './components/SearchBar';
import ElementFilter from './components/ElementFilter';
import Loading from './components/Loading';
import Error from './components/Error';

const API_BASE_URL = 'http://localhost:5000/api';

function App() {
  const [zodiacs, setZodiacs] = useState([]);
  const [filteredZodiacs, setFilteredZodiacs] = useState([]);
  const [selectedZodiac, setSelectedZodiac] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedElement, setSelectedElement] = useState('');
  const [elements, setElements] = useState([]);

  // Fetch all zodiacs on component mount
  useEffect(() => {
    const fetchZodiacs = async () => {
      try {
        setLoading(true);
        setError(null);
        const response = await axios.get(`${API_BASE_URL}/zodiacs`);
        
        if (response.data.success) {
          setZodiacs(response.data.data);
          setFilteredZodiacs(response.data.data);
        } else {
          setError('Failed to load zodiac signs');
        }
      } catch (err) {
        setError(err.response?.data?.error || 'Error fetching zodiacs: ' + err.message);
      } finally {
        setLoading(false);
      }
    };

    const fetchElements = async () => {
      try {
        const response = await axios.get(`${API_BASE_URL}/elements`);
        if (response.data.success) {
          setElements(response.data.data);
        }
      } catch (err) {
        console.error('Error fetching elements:', err);
      }
    };

    fetchZodiacs();
    fetchElements();
  }, []);

  // Handle search
  const handleSearch = (query) => {
    setSearchQuery(query);
    filterZodiacs(query, selectedElement);
  };

  // Handle element filter
  const handleElementFilter = (element) => {
    setSelectedElement(element);
    filterZodiacs(searchQuery, element);
  };

  // Filter zodiacs based on search and element
  const filterZodiacs = (query, element) => {
    let results = zodiacs;

    if (query.trim()) {
      results = results.filter(z =>
        z.name.toLowerCase().includes(query.toLowerCase())
      );
    }

    if (element) {
      results = results.filter(z => z.element === element);
    }

    setFilteredZodiacs(results);
  };

  // Get random zodiac
  const handleRandomZodiac = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await axios.get(`${API_BASE_URL}/zodiacs/random`);
      
      if (response.data.success) {
        setSelectedZodiac(response.data.data);
      } else {
        setError('Failed to load random zodiac');
      }
    } catch (err) {
      setError('Error fetching random zodiac: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  // Handle card click
  const handleCardClick = (zodiac) => {
    setSelectedZodiac(zodiac);
  };

  // Close modal
  const handleCloseModal = () => {
    setSelectedZodiac(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-600 via-purple-700 to-indigo-900 py-8 px-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <header className="text-center mb-12">
          <h1 className="text-5xl md:text-6xl font-bold text-white mb-4 drop-shadow-lg">
            ✨ Zodiac Explorer
          </h1>
          <p className="text-xl text-purple-100 drop-shadow-md">
            Discover the stars and your cosmic destiny
          </p>
        </header>

        {/* Controls */}
        <div className="mb-8">
          <SearchBar 
            value={searchQuery}
            onChange={handleSearch}
            placeholder="Search zodiac signs..."
          />
          <div className="mt-6 flex flex-col md:flex-row gap-4 items-center justify-center">
            <ElementFilter
              elements={elements}
              selectedElement={selectedElement}
              onFilter={handleElementFilter}
            />
            <button
              onClick={handleRandomZodiac}
              className="px-6 py-3 bg-yellow-400 hover:bg-yellow-500 text-gray-900 font-bold rounded-lg shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200"
            >
              🎲 Random Zodiac
            </button>
          </div>
        </div>

        {/* Error State */}
        {error && <Error message={error} />}

        {/* Loading State */}
        {loading && <Loading />}

        {/* Zodiacs Grid */}
        {!loading && !error && (
          <>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 mb-8">
              {filteredZodiacs.length > 0 ? (
                filteredZodiacs.map(zodiac => (
                  <ZodiacCard
                    key={zodiac.id}
                    zodiac={zodiac}
                    onClick={() => handleCardClick(zodiac)}
                  />
                ))
              ) : (
                <div className="col-span-full text-center py-12">
                  <p className="text-2xl text-white">
                    No zodiac signs found. Try a different search!
                  </p>
                </div>
              )}
            </div>

            {/* Results Count */}
            {filteredZodiacs.length > 0 && (
              <div className="text-center mb-6">
                <p className="text-white text-lg font-semibold">
                  Showing {filteredZodiacs.length} of {zodiacs.length} zodiac signs
                </p>
              </div>
            )}
          </>
        )}
      </div>

      {/* Modal */}
      {selectedZodiac && (
        <ZodiacModal
          zodiac={selectedZodiac}
          onClose={handleCloseModal}
        />
      )}
    </div>
  );
}

export default App;
