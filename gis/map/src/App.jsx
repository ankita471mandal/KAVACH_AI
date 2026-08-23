import "./App.css";
import RiskMap from "./components/map/RiskMap";

function App() {
  return (
    <div className="app">
      <h1>KAVACH AI — GIS Map</h1>

      <div className="map-container">
        <RiskMap />
      </div>
    </div>
  );
}

export default App;