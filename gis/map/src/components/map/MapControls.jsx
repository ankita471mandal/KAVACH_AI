import { LayersControl } from "react-leaflet";

function MapControls({ children }) {
  return (
    <LayersControl position="topright">
      {children}
    </LayersControl>
  );
}

export default MapControls;