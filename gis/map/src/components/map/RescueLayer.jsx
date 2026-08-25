import { CircleMarker, Popup } from "react-leaflet";
import rescueData from "../../../../data/rescue_teams.geojson?raw";

const rescueTeams = JSON.parse(rescueData);

function RescueLayer() {
  return (
    <>
      {rescueTeams.features.map((team) => {
        const [longitude, latitude] = team.geometry.coordinates;
        const p = team.properties;

        return (
          <CircleMarker
            key={p.team_id}
            center={[latitude, longitude]}
            radius={8}
            pathOptions={{
              color: "#7e22ce",
              fillColor: "#a855f7",
              fillOpacity: 0.9
            }}
          >
            <Popup>
              <strong>{p.team_name}</strong>
              <br />
              Team ID: {p.team_id}
              <br />
              Members: {p.members}
              <br />
              Status: {p.status}
              <br />
              Mission: {p.mission}
            </Popup>
          </CircleMarker>
        );
      })}
    </>
  );
}

export default RescueLayer;