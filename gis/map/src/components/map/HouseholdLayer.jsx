import { CircleMarker, Popup } from "react-leaflet";
import householdsData from "../../../../data/households.geojson?raw";

const households = JSON.parse(householdsData);

function HouseholdLayer() {
  return (
    <>
      {households.features.map((household) => {
        const [longitude, latitude] = household.geometry.coordinates;
        const p = household.properties;

        return (
          <CircleMarker
            key={p.household_id}
            center={[latitude, longitude]}
            radius={6}
            pathOptions={{
              color: "#a16207",
              fillColor: "#eab308",
              fillOpacity: 0.9
            }}
          >
            <Popup>
              <strong>Household {p.household_id}</strong>
              <br />
              Members: {p.members}
              <br />
              Vulnerable members: {p.vulnerable_members}
              <br />
              Status: {p.status}
            </Popup>
          </CircleMarker>
        );
      })}
    </>
  );
}

export default HouseholdLayer;