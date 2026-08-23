import { GeoJSON } from "react-leaflet"; 
 
const zones = { 
  type: "FeatureCollection", 
  features: [ 
    { 
      type: "Feature", 
      properties: { 
        zone_id: "Z17", 
        risk_score: 87, 
        risk_level: "CRITICAL", 
        population: 426, 
        vulnerable_households: 38, 
        updated_at: "2026-08-23T10:30:00" 
      }, 
      geometry: { 
        type: "Polygon", 
        coordinates: [ 
          [ 
            [88.360, 22.570], 
            [88.375, 22.570], 
            [88.375, 22.585], 
            [88.360, 22.585], 
            [88.360, 22.570] 
          ] 
        ] 
      } 
    } 
  ] 
}; 
 
function RiskZoneLayer() { 
  const styleZone = () => ({ 
    color: "#b91c1c", 
    weight: 2, 
    fillColor: "#ef4444", 
    fillOpacity: 0.35 
  }); 
 
  const onEachZone = (feature, layer) => { 
    const p = feature.properties; 
 
    layer.bindPopup(` 
      <strong>Zone ${p.zone_id}</strong><br/> 
      Risk: ${p.risk_score}<br/> 
      Level: ${p.risk_level}<br/> 
      Population: ${p.population}<br/> 
      Vulnerable households: ${p.vulnerable_households}<br/> 
      Last updated: ${p.updated_at} 
    `); 
  }; 
 
  return ( 
    <GeoJSON 
      data={zones} 
      style={styleZone} 
      onEachFeature={onEachZone} 
    /> 
  ); 
} 
 
export default RiskZoneLayer;                                          