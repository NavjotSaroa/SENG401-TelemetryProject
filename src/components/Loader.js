// src/components/Loader.js
const Loader = () => {
    return (
      <div className="loader-container">
        <div className="spinner-border text-danger" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
      </div>
    );
  };
  
  export default Loader;