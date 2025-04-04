import { BrowserRouter, Route, Routes } from "react-router-dom";
import MasterLayout from "./masterLayout/MasterLayout";
import DashBoardLayerOne from "./lens/DashBoardLayerOne";
import DashBoardLayerTwo from "./spark/DashBoardLayerTwo";
import MarketplaceLayer from "./next/MarketplaceLayer";
import SignInLayer from "./vita/SignInLayer";
import SignUpLayer from "./vita/SignUpLayer";

function App() {
  return (
    <BrowserRouter>
      <MasterLayout>
        <Routes>
          <Route path='/' element={<DashBoardLayerOne />} />
          <Route path='/lens' element={<DashBoardLayerOne />} />
          <Route path='/spark' element={<DashBoardLayerTwo />} />
          <Route path='/next' element={<MarketplaceLayer />} />
          <Route path='/signin' element={<SignInLayer />} />
          <Route path='/signup' element={<SignUpLayer />} />
        </Routes>
      </MasterLayout>
    </BrowserRouter>
  );
}

export default App;
