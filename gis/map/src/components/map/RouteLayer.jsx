import { GeoJSON } from "react-leaflet";
import routesData from "../../../../data/routes.geojson?raw";

const routes = JSON.parse(routesData);

function RouteLayer() {
  const styleRoute = () => ({
    color: "#16a34a",
    weight: 7,
    opacity: 0.9
  });

  const onEachRoute = (feature, layer) => {
    const p = feature.properties;

    layer.bindPopup(`
      <strong>Evacuation Route ${p.route_id}</strong><br/>
      Distance: ${p.distance_km} km<br/>
      ETA: ${p.estimated_minutes} minutes<br/>
      Safety Score: ${p.safety_score}/100<br/>
      Status: ${p.status}
    `);
  };

  return (
    <GeoJSON
      data={routes}
      style={styleRoute}
      onEachFeature={onEachRoute}
    />
  );
}

export default RouteLayer;