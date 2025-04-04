import './styles/bootstrap.min.css';
import './styles/style.css';
import './styles/extra.css';
import React from "react";
import ReactDOM from "react-dom/client";
import 'quill/dist/quill.snow.css';
import "jsvectormap/dist/css/jsvectormap.css";
import 'react-toastify/dist/ReactToastify.css';
import 'react-modal-video/css/modal-video.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import App from "./App";
import reportWebVitals from "./reportWebVitals";


const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <>
    <App />
  </>
);

reportWebVitals();
