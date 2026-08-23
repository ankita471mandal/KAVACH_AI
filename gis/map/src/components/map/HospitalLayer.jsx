import { CircleMarker, Popup } from "react-leaflet";
import hospitalsData from "../../../../data/hospitals.geojson?raw";

const hospitals = JSON.parse(hospitalsData);
function HospitalLayer() {
  return (
    <>
      {hospitals.features.map((hospital) => {
        const [longitude, latitude] = hospital.geometry.coordinates;
        const p = hospital.properties;

        return (
          <CircleMarker
            key={p.hospital_id}
            center={[latitude, longitude]}
            radius={9}
            pathOptions={{
              color: "#1d4ed8",
              fillColor: "#3b82f6",
              fillOpacity: 0.9,
              weight: 2,
            }}
          >
            <Popup>
              <div>
                <strong>{p.name}</strong>
                <br />
                Hospital ID: {p.hospital_id}
                <br />
                Emergency: {p.emergency ? "Yes" : "No"}
                <br />
                Beds available: {p.beds_available}
                <br />
                ICU available: {p.icu_available}
                <br />
                Ambulances: {p.ambulances}
                <br />
                Status: {p.status}
              </div>
            </Popup>
          </CircleMarker>
        );
      })}
    </>
  );
}

export default HospitalLayer;