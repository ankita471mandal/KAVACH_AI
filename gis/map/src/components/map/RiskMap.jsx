import {
  MapContainer,
  TileLayer,
  LayersControl
} from "react-leaflet";

import "leaflet/dist/leaflet.css";

import RiskZoneLayer from "./RiskZoneLayer";
import HospitalLayer from "./HospitalLayer";
import ShelterLayer from "./ShelterLayer";
import HouseholdLayer from "./HouseholdLayer";
import RoadLayer from "./RoadLayer";
import RescueLayer from "./RescueLayer";
import SOSLayer from "./SOSLayer";
import RouteLayer from "./RouteLayer";

function RiskMap() {
  return (
    <MapContainer
      center={[22.575, 88.37]}
      zoom={14}
      scrollWheelZoom={true}
      style={{
        height: "650px",
        width: "100%"
      }}
    >

      {/* Base Map */}
      <TileLayer
        attribution="&copy; OpenStreetMap contributors"
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      {/* Layer Controls */}
      <LayersControl position="topright">

        <LayersControl.Overlay
          checked
          name="🔴 Risk Zones"
        >
          <RiskZoneLayer />
        </LayersControl.Overlay>

        <LayersControl.Overlay
          checked
          name="🔵 Hospitals"
        >
          <HospitalLayer />
        </LayersControl.Overlay>

        <LayersControl.Overlay
          checked
          name="🟢 Shelters"
        >
          <ShelterLayer />
        </LayersControl.Overlay>

        <LayersControl.Overlay
          checked
          name="🟡 Households"
        >
          <HouseholdLayer />
        </LayersControl.Overlay>

        <LayersControl.Overlay
          checked
          name="⚫ Roads"
        >
          <RoadLayer />
        </LayersControl.Overlay>

        <LayersControl.Overlay
          checked
          name="🟣 Rescue Teams"
        >
          <RescueLayer />
        </LayersControl.Overlay>

        <LayersControl.Overlay
          checked
          name="🚨 SOS"
        >
          <SOSLayer />
        </LayersControl.Overlay>

        <LayersControl.Overlay
          checked
          name="━━ Evacuation Route"
        >
          <RouteLayer />
        </LayersControl.Overlay>

      </LayersControl>

    </MapContainer>
  );
}

export default RiskMap;