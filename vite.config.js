import { defineConfig } from 'vite';
import path from 'path';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  plugins: [
    tailwindcss()
  ],  
  base: '/static/', // This should match Django's settings.STATIC_URL
  build: {
    // Where Vite will save its output files.
    // This should be something in your settings.STATICFILES_DIRS
    outDir: path.resolve(__dirname, './static'),
    emptyOutDir: false, // Preserve the outDir to not clobber Django's other files.
    manifest: "manifest.json",
    rollupOptions: {
      input: {
        'main': path.resolve(__dirname, 'assets/js/main.ts'),
        'flatpickr': path.resolve(__dirname, 'assets/src/flatpickr_init.ts'),
        'styles': path.resolve(__dirname, 'assets/src/styles.css'),
      },
      output: {
        // Output JS bundles to js/ directory with -bundle suffix
        entryFileNames: `js/[name]-bundle.js`,
      },
    },
  },
});