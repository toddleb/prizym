import React from 'react';
import { createRoot } from 'react-dom/client';
import SimpleApp from './SimpleApp.js';

// Proper React 18 method
const container = document.getElementById('root');
const root = createRoot(container);

// Just rendering the absolute simplest thing possible
root.render(<div>Hello World</div>);