import { CircleMarker, Popup } from "react-leaflet";
import sheltersData from "../../../../data/shelters.geojson?raw";

const shelters = JSON.parse(sheltersData);

function ShelterLayer() {
  return (
    <>
      {shelters.features.map((shelter) => {
        const [longitude, latitude] = shelter.geometry.coordinates;
        const p = shelter.properties;

        return (
          <CircleMarker
            key={p.shelter_id}
            center={[latitude, longitude]}
            radius={9}
            pathOptions={{
              color: "#166534",
              fillColor: "#22c55e",
              fillOpacity: 0.9,
              weight: 2,
            }}
          >
            <Popup>
              <strong>{p.name}</strong>
              <br />
              Shelter ID: {p.shelter_id}
              <br />
              Capacity: {p.capacity}
              <br />
              Occupancy: {p.occupancy}
              <br />
              Available: {p.available}
              <br />
              Status: {p.status}
            </Popup>
          </CircleMarker>
        );
      })}
    </>
  );
}

export default ShelterLayer;