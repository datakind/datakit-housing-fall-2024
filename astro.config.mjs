import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import tailwind from "@astrojs/tailwind";

// https://astro.build/config
export default defineConfig({
  site: 'https://datakind.github.io',
  base: '/datakit-housing',
  integrations: [starlight({
    title: 'DataKit™',
    description: 'Affordable Housing, September 2024',
    favicon: '/favicon.svg',
	customCss: [
		'./src/styles/custom.css'
	],
	social: {
      github: 'https://github.com/datakind/datakit-housing'
    },
    sidebar: [{
      label: 'Getting Started',
      items: [
        {
          label: 'What\'s a DataKit?',
          slug: 'data-kit'
        },
        {
        label: 'Problem to tackle',
        slug: 'problem-to-tackle'
      },
	    {
        label: 'Accessing the data',
        slug: 'accessing-the-data'
      },
	    {
        label: 'Submitting your work',
        slug: 'submitting-your-work'
      },
      {
        label: "Code of conduct",
        slug: 'code-of-conduct'
      }]
    },
	{
      label: 'Resources',
      items: [
        {
          label: 'Housing data',
          slug: 'housing-data'
        },
        {
          label: 'FAQs',
          slug: 'faqs'
        }]
    }]
  }), tailwind({
	applyBaseStyles: false
  })]
});