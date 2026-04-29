/* vtt-seo.js · VLADS TEST TARGET
 * ─────────────────────────────────────────────────────────────────────────
 * Injects SEO meta tags, Open Graph tags, canonical URL, and JSON-LD
 * structured data into every page automatically based on the current
 * filename. Add one line to each page's <head>:
 *
 *   <script src="../vtt-seo.js"></script>
 *
 * Note: robots.txt and sitemap.xml must sit at the GitHub Pages root
 * (play-orange/), not inside v1/. If GitHub Pages serves from the repo
 * root, place robots.txt there.
 * ─────────────────────────────────────────────────────────────────────────
 */

(function () {
  'use strict';

  const BASE_URL  = 'https://vsaddr-github.github.io/play-orange/v1';
  const OG_IMAGE  = BASE_URL + '/vtt-og-image.jpg';   /* 1200×630px — add this file to the repo */
  const SITE_NAME = "VLADS TEST TARGET — Film Scanning Academy";
  const AUTHOR    = "Vlads Test Target";

  /* ── per-page metadata ────────────────────────────────────────────────── */
  const pages = {
    'film4ever.html': {
      title:       'Film Scanning Academy — Interactive Diagrams · VLADS TEST TARGET',
      description: 'A collection of interactive diagrams explaining the science physics of film scanning — chromogenic dye behaviour, linear capture, sensor wells, gamma encoding, and the orange mask. For photographers who scan film.',
      type:        'WebSite',
      keywords:    'film scanning, color negative, orange mask, chromogenic dye, linear capture, camera scanning, analog photography'
    },
    'graph1.html': {
      title:       'H&D Curve → Electron Well Fill · Graph 1 · VLADS TEST TARGET',
      description: 'Interactive Hurter-Driffield characteristic curve showing how scene log exposure maps to film density and into 14-bit sensor electron counts. Why equal density steps produce unequal electron counts — and what this means for scanning.',
      type:        'LearningResource',
      keywords:    'H&D curve, characteristic curve, film density, electron well, 14-bit sensor, transmittance, toe shoulder film, film scanning Academy'
    },
    'graph2.html': {
      title:       'Electron Count → Display Brightness · Graph 2 · VLADS TEST TARGET',
      description: 'Interactive diagram showing how raw sensor electron counts map to screen brightness — and why gamma encoding is the difference between correct tonal rendering and crushed shadows. Linear vs sRGB compared.',
      type:        'LearningResource',
      keywords:    'gamma encoding, sRGB, display brightness, linear sensor, electron count, gamma 2.2, film scanning pipeline'
    },
    'graph22.html': {
      title:       'Electron Well Zone Limits · Graph 22 · VLADS TEST TARGET',
      description: 'How much of a 14-bit sensor well a colour negative actually uses — and where the linear zone of the H&D curve lands within that fraction. Wasted headroom, wasted floor, and the case for exposing to the right when scanning.',
      type:        'LearningResource',
      keywords:    'sensor dynamic range, Dmin Dmax, electron well capacity, linear zone, film scanning exposure, 14-bit raw, color negative scanning'
    },
    'graph3.html': {
      title:       'Linear Space → Inversion → Display · Graph 3 · VLADS TEST TARGET',
      description: 'Why negative inversion must happen in linear space — and how a Lightroom import tone curve applied before inversion permanently destroys toe and shoulder detail. The correct and incorrect pipeline compared interactively.',
      type:        'LearningResource',
      keywords:    'negative inversion, linear profile, Lightroom import, tone curve, film scanning workflow, color negative inversion, linear capture'
    },
    'graph4.html': {
      title:       'Chromogenic Dyes & the Orange Mask · Graph 4 · VLADS TEST TARGET',
      description: 'Interactive spectral diagram showing how cyan, magenta and yellow dye layers form from colored couplers during development — and why the residual coupler absorption produces the orange mask. Drag the exposure slider to see dye vs coupler balance.',
      type:        'LearningResource',
      keywords:    'orange mask, chromogenic dye, color coupler, color negative film, cyan dye, magenta dye, yellow dye, film chemistry, color negative scanning'
    },
    'graph5.html': {
      title:       'Film Absorption × Illuminant Interaction · Graph 5 · VLADS TEST TARGET',
      description: 'What the scanner sensor actually receives — film transmission multiplied by the backing light spectrum. Adjust colour temperature from 3000K tungsten to 15000K blue sky and see how the orange mask dominates regardless of light source.',
      type:        'LearningResource',
      keywords:    'film transmission, illuminant spectrum, colour temperature, scanning light source, orange mask, LED panel film scanning, blackbody spectrum, film scanning science'
    },
    'glossary.html': {
      title:       'Sensor Terminology Glossary · VLADS TEST TARGET',
      description: 'Standard vocabulary used in digital sensor exercises — photosites, electron wells, full well capacity, ADC, digital number, read noise, shot noise, SNR, quantum efficiency. Every term used across the film scanning physics series defined in one place.',
      type:        'DefinedTermSet',
      keywords:    'photosite, electron well, full well capacity, read noise, shot noise, SNR, quantum efficiency, ADC, digital number, sensor terminology, camera sensor science'
    }
  };

  /* ── resolve current page ─────────────────────────────────────────────── */
  const filename = window.location.pathname.split('/').pop() || 'film4ever.html';
  const page     = pages[filename] || pages['film4ever.html'];
  const pageURL  = BASE_URL + '/' + filename;

  /* ── helper: create and append a <meta> tag ───────────────────────────── */
  function meta(attrs) {
    const el = document.createElement('meta');
    Object.entries(attrs).forEach(([k, v]) => el.setAttribute(k, v));
    document.head.appendChild(el);
  }

  /* ── helper: create and append a <link> tag ───────────────────────────── */
  function link(attrs) {
    const el = document.createElement('link');
    Object.entries(attrs).forEach(([k, v]) => el.setAttribute(k, v));
    document.head.appendChild(el);
  }

  /* ── set <title> if not already a good one ────────────────────────────── */
  if (!document.title || document.title === '') {
    document.title = page.title;
  }

  /* ── standard meta ────────────────────────────────────────────────────── */
  meta({ name: 'description',        content: page.description });
  meta({ name: 'author',             content: AUTHOR });
  meta({ name: 'keywords',           content: page.keywords });
  meta({ name: 'robots',             content: 'index, follow' });
  meta({ name: 'theme-color',        content: '#f5f2ec' });

  /* ── canonical ────────────────────────────────────────────────────────── */
  link({ rel: 'canonical', href: pageURL });

  /* ── Open Graph ───────────────────────────────────────────────────────── */
  meta({ property: 'og:type',        content: 'article' });
  meta({ property: 'og:site_name',   content: SITE_NAME });
  meta({ property: 'og:title',       content: page.title });
  meta({ property: 'og:description', content: page.description });
  meta({ property: 'og:url',         content: pageURL });
  meta({ property: 'og:image',       content: OG_IMAGE });
  meta({ property: 'og:image:width', content: '1200' });
  meta({ property: 'og:image:height',content: '630' });
  meta({ property: 'og:locale',      content: 'en_US' });

  /* ── Twitter / X card ─────────────────────────────────────────────────── */
  meta({ name: 'twitter:card',        content: 'summary_large_image' });
  meta({ name: 'twitter:title',       content: page.title });
  meta({ name: 'twitter:description', content: page.description });
  meta({ name: 'twitter:image',       content: OG_IMAGE });
  meta({ name: 'twitter:site',        content: '@vladstesttarget' });

  /* ── JSON-LD structured data ──────────────────────────────────────────── */
  const isIndex = filename === 'film4ever.html';

  const jsonld = isIndex ? {
    '@context':   'https://schema.org',
    '@type':      'WebSite',
    'name':       SITE_NAME,
    'url':        pageURL,
    'description': page.description,
    'author': {
      '@type': 'Person',
      'name':  AUTHOR,
      'url':   'https://www.film4ever.info/home'
    },
    'publisher': {
      '@type': 'Person',
      'name':  AUTHOR
    }
  } : {
    '@context':   'https://schema.org',
    '@type':      page.type || 'LearningResource',
    'name':       page.title,
    'description': page.description,
    'url':        pageURL,
    'isPartOf': {
      '@type': 'WebSite',
      'name':  SITE_NAME,
      'url':   BASE_URL + '/film4ever.html'
    },
    'author': {
      '@type': 'Person',
      'name':  AUTHOR,
      'url':   'https://www.film4ever.info/home'
    },
    'educationalUse':    'instruction',
    'learningResourceType': 'interactive resource',
    'audience': {
      '@type': 'EducationalAudience',
      'educationalRole': 'student'
    },
    'inLanguage': 'en'
  };

  const script = document.createElement('script');
  script.type        = 'application/ld+json';
  script.textContent = JSON.stringify(jsonld, null, 2);
  document.head.appendChild(script);

}());
