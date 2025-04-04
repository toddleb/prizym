import fs from 'fs';
import path from 'path';

const slidesDir = './src/components/slides/Prizym_AIFramework';

// Read all slide files (ignoring index.jsx)
const slideFiles = fs.readdirSync(slidesDir).filter(file => file.endsWith('.jsx') && file !== 'index.jsx');

slideFiles.forEach((file) => {
  const match = file.match(/^(\d+)_([\w\d_]+)\.jsx$/);
  if (!match) {
    console.log(`Skipping ${file} - doesn't match naming pattern.`);
    return;
  }

  const slideNumber = parseInt(match[1], 10);
  const componentName = match[2];

  const filePath = path.join(slidesDir, file);
  
  const slideContent = `import React from 'react';

const ${componentName} = ({ slideNumber }) => (
  <div className="slide">
    <h1 className="slide-title">
      Slide {slideNumber}: ${componentName.replace(/_/g, ' ')}
    </h1>
    {/* Your slide content here */}
  </div>
);

export default ${componentName};
`;

  fs.writeFileSync(filePath, slideContent, 'utf-8');
  console.log(`✅ Updated slide ${file}`);
});

console.log('🎉 All slides updated successfully!');
