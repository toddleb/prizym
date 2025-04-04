// pages/_document.tsx
import { Html, Head, Main, NextScript } from 'next/document';
import { ColorModeScript } from '@chakra-ui/react';
import theme from '../theme';

export default function Document() {
  return (
    <Html lang="en">
      <Head>
        {/* Cosmic Fonts */}
        <link
          href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500&family=Poppins&display=swap"
          rel="stylesheet"
        />
        <meta name="theme-color" content="#0b0c2a" />
        <meta name="description" content="Star Navigator – Discover your constellation career path" />
        {/* Favicon placeholder */}
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <body>
        {/* Chakra color mode init */}
        <ColorModeScript initialColorMode={theme.config.initialColorMode} />
        <Main />
        <NextScript />
      </body>
    </Html>
  );
}