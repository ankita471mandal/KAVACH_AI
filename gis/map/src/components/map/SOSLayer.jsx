import { CircleMarker, Popup } from "react-leaflet";
import sosData from "../../../../data/sos.geojson?raw";

const sosRequests = JSON.parse(sosData);

function SOSLayer() {
  return (
    <>
      {sosRequests.features.map((sos) => {
        const [longitude, latitude] = sos.geometry.coordinates;
        const p = sos.properties;

        return (
          <CircleMarker
            key={p.sos_id}
            center={[latitude, longitude]}
            radius={10}
            pathOptions={{
              color: "#991b1b",
              fillColor: "#ef4444",
              fillOpacity: 1,
              weight: 3
            }}
          >
            <Popup>
              <strong>🚨 SOS {p.sos_id}</strong>
              <br />
              Severity: {p.severity}
              <br />
              Message: {p.message}
              <br />
              Status: {p.status}
            </Popup>
          </CircleMarker>
        );
      })}
    </>
  );
}

export default SOSLayer;