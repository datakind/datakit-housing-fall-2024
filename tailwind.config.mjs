import defaultTheme from 'tailwindcss/defaultTheme';
import starlightPlugin from '@astrojs/starlight-tailwind';


/** @type {import('tailwindcss').Config} */
export default {
	content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
    theme: {
        extend: {
            fontFamily: {
                sans: ['Figtree', ...defaultTheme.fontFamily.sans],
            },
            colors: {
				primary: {
                    DEFAULT: '#f79122',
                    dark: '#e37425',
                    light: '#f9aa62',
                },
                secondary: {
                    DEFAULT: '#385981',
                    dark: '#2f3c5b',
                    light: '#87b7cc',
                },
                link: {
                    DEFAULT: '#3596cd',
                },
                gray: {
                    DEFAULT: '#303030',
                    dark: '#606060',
                    light: '#959595',
                },
                green: {
                    DEFAULT: '#25A95A',
                },
                red: {
                    DEFAULT: '#A92532',
                },
                background: {
                    DEFAULT: '#f1f1f1',
                    light: '#ffffff',
                },
            },
        },
		plugins: [starlightPlugin()]
    },
};