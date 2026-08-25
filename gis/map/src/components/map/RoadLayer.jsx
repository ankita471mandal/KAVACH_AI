import { GeoJSON } from "react-leaflet";
import roadsData from "../../../../data/roads.geojson?raw";

const roads = JSON.parse(roadsData);

function RoadLayer() {
  const styleRoad = (feature) => ({
    color: feature.properties.status === "BLOCKED" ? "#dc2626" : "#111827",
    weight: 5,
    opacity: 0.8,
    dashArray: feature.properties.status === "BLOCKED" ? "8, 8" : undefined
  });

  const onEachRoad = (feature, layer) => {
    const p = feature.properties;

    layer.bindPopup(`
      <strong>${p.name}</strong><br/>
      Road ID: ${p.road_id}<br/>
      Status: ${p.status}
    `);
  };

  return (
    <GeoJSON
      data={roads}
      style={styleRoad}
      onEachFeature={onEachRoad}
    />
  );
}

export default RoadLayer;