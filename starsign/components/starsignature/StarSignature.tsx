import React, { useEffect, useRef } from 'react';

interface SkillScore {
  name: string;
  score: number; // from 0 to 100
}

interface StarSignatureProps {
  skills: SkillScore[];
  radius?: number;
  strokeColor?: string;
  fillColor?: string;
  primaryConstellation?: string;
  risingSigns?: string[];
  animate?: boolean;
  showTooltips?: boolean;
  comparisonSkills?: SkillScore[];
  exportId?: string;
}

const StarSignature: React.FC<StarSignatureProps> = ({
  skills,
  radius = 100,
  strokeColor = '#8F00FF',
  fillColor = 'rgba(143, 0, 255, 0.3)',
  primaryConstellation,
  risingSigns = [],
  animate = true,
  showTooltips = true,
  comparisonSkills,
  exportId = 'star-signature-svg',
}) => {
  const center = radius + 60;
  const angleSlice = (2 * Math.PI) / skills.length;
  const polygonRef = useRef<SVGPolygonElement>(null);
  const svgRef = useRef<SVGSVGElement>(null);

  const getPoints = (data: SkillScore[]) =>
    data.map((skill, i) => {
      const angle = i * angleSlice - Math.PI / 2;
      const r = (skill.score / 100) * radius;
      const x = center + r * Math.cos(angle);
      const y = center + r * Math.sin(angle);
      return { x, y, label: skill.name, value: skill.score };
    });

  const mainPoints = getPoints(skills);
  const comparisonPoints = comparisonSkills ? getPoints(comparisonSkills) : null;

  const polygonPoints = mainPoints.map(p => `${p.x},${p.y}`).join(' ');
  const comparisonPolygonPoints = comparisonPoints?.map(p => `${p.x},${p.y}`).join(' ');

  useEffect(() => {
    if (!animate || !polygonRef.current) return;
    const polygon = polygonRef.current;
    polygon.style.opacity = '0';
    polygon.style.transform = 'scale(0.6)';
    polygon.style.transition = 'opacity 0.5s ease, transform 0.6s ease';
    setTimeout(() => {
      polygon.style.opacity = '1';
      polygon.style.transform = 'scale(1)';
    }, 50);
  }, [animate]);

  const spokeLines = skills.map((_, i) => {
    const angle = i * angleSlice - Math.PI / 2;
    const x = center + radius * Math.cos(angle);
    const y = center + radius * Math.sin(angle);
    return <line key={i} x1={center} y1={center} x2={x} y2={y} stroke="#444" strokeDasharray="2 2" />;
  });

  const labels = skills.map((skill, i) => {
    const angle = i * angleSlice - Math.PI / 2;
    const labelRadius = radius + 35;
    const x = center + labelRadius * Math.cos(angle);
    const y = center + labelRadius * Math.sin(angle);
    return (
      <text
        key={i}
        x={x}
        y={y}
        textAnchor="middle"
        alignmentBaseline="middle"
        fontSize="11"
        fill="#ccc"
      >
        {skill.name}
      </text>
    );
  });

  const stars = Array.from({ length: 40 }, (_, i) => {
    const x = Math.random() * center * 2;
    const y = Math.random() * center * 2;
    const r = Math.random() * 1.2 + 0.3;
    return <circle key={i} cx={x} cy={y} r={r} fill="#fff" opacity={Math.random() * 0.4 + 0.2} />;
  });

  const handleExport = () => {
    if (!svgRef.current) return;
    const svg = svgRef.current;
    const serializer = new XMLSerializer();
    const source = serializer.serializeToString(svg);
    const blob = new Blob([source], { type: 'image/svg+xml;charset=utf-8' });
    const url = URL.createObjectURL(blob);

    const a = document.createElement('a');
    a.href = url;
    a.download = `${primaryConstellation || 'StarSignature'}.svg`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div style={{ textAlign: 'center', background: '#000', padding: '1rem', borderRadius: '12px' }}>
      <svg ref={svgRef} id={exportId} width={center * 2} height={center * 2}>
        <defs>
          <radialGradient id="starburst" cx="50%" cy="50%" r="100%">
            <stop offset="0%" stopColor="#ffffff" stopOpacity="0.1" />
            <stop offset="100%" stopColor="#8F00FF" stopOpacity="0.2" />
          </radialGradient>
        </defs>

        <rect width="100%" height="100%" fill="#000" />
        <g>{stars}</g>
        <circle cx={center} cy={center} r={radius + 10} fill="url(#starburst)" />

        <g>
          {spokeLines}

          {comparisonPolygonPoints && (
            <polygon
              points={comparisonPolygonPoints}
              stroke="#00BFFF"
              fill="rgba(0, 191, 255, 0.2)"
              strokeWidth={1.5}
              strokeDasharray="5 3"
            />
          )}

          <polygon
            ref={polygonRef}
            points={polygonPoints}
            stroke={strokeColor}
            fill={fillColor}
            strokeWidth={2}
          />

          {showTooltips &&
            mainPoints.map((p, i) => (
              <circle key={i} cx={p.x} cy={p.y} r={3} fill={strokeColor}>
                <title>{`${p.label}: ${p.value}`}</title>
              </circle>
            ))}

          {labels}

          {primaryConstellation && (
            <text
              x={center}
              y={center - 10}
              textAnchor="middle"
              fontSize="18"
              fill="#8F00FF"
              fontWeight="bold"
            >
              {primaryConstellation}
            </text>
          )}
          {risingSigns.length > 0 && (
            <text
              x={center}
              y={center + 18}
              textAnchor="middle"
              fontSize="11"
              fill="#aaa"
            >
              Rising: {risingSigns.join(', ')}
            </text>
          )}
        </g>
      </svg>

      <button
        onClick={handleExport}
        style={{
          marginTop: '1rem',
          backgroundColor: '#8F00FF',
          color: '#fff',
          border: 'none',
          borderRadius: '8px',
          padding: '8px 16px',
          cursor: 'pointer',
          fontSize: '0.9rem',
        }}
      >
        Export as SVG
      </button>
    </div>
  );
};

export default StarSignature;

