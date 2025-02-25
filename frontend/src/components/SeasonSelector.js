// src/components/SeasonSelector.js

const SeasonSelector = ({ onSeasonSelect, minYear = 2019, maxYear = 2024 }) => {
  const handleSeasonChange = (e) => {
    const season = e.target.value;
    onSeasonSelect(season);
  };

  return (
    <div className="season-selector mb-4">
      <label className="form-label">Select F1 Season:</label>
      <select 
        className="form-select"
        defaultValue=""
        onChange={handleSeasonChange}
      >
        <option value="" disabled>Choose a season</option>
        {Array.from({ length: maxYear - minYear + 1 }, (_, i) => minYear + i).map((season) => (
          <option key={season} value={season}>{season}</option>
        ))}
      </select>
    </div>
  );
};

export default SeasonSelector;
