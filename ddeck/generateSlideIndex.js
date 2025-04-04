import fs from 'fs';
import path from 'path';

const slidesDir = './src/components/slides/Prizym_AIFramework';
const indexPath = path.join(slidesDir, 'index.jsx');

const files = fs.readdirSync(slidesDir)
  .filter(file => file.endsWith('.jsx') && file !== 'index.jsx')
  .sort((a, b) => parseInt(a) - parseInt(b));

let imports = "import React from 'react';\n\n";
let slideArray = 'const SlideLibrary = [\n';

files.forEach((file) => {
  const match = file.match(/^(\d+)_([\w\d_]+)\.jsx$/);
  if (match) {
    const slideNumber = parseInt(match[1], 10);
    const componentName = match[2];
    const importName = `${componentName}`;

    imports += `import ${importName} from './${file.replace('.jsx', '')}';\n`;
    slideArray += `  { name: '${componentName}', component: () => <${importName} slideNumber={${slideNumber}} /> },\n`;
  }
});

slideArray += '];\n\nexport default SlideLibrary;\n';

fs.writeFileSync(indexPath, imports + '\n' + slideArray);
console.log(`🎉 Slide index generated successfully at ${indexPath}`);
