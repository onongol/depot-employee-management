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
        'amount_inputs': path.resolve(__dirname, 'assets/js/amount/amount_inputs.js'),
        'amount_validation': path.resolve(__dirname, 'assets/js/amount/amount_validation.js'),
        'password_toggle': path.resolve(__dirname, 'assets/js/auth/password_toggle.js'),
        'checkbox_validation': path.resolve(__dirname, 'assets/js/checkbox/checkbox_validation.js'),
        'select_all': path.resolve(__dirname, 'assets/js/checkbox/select_all.js'),
        'department_dropdown': path.resolve(__dirname, 'assets/js/dropdowns/department_dropdown.js'),
        'user_dropdown': path.resolve(__dirname, 'assets/js/dropdowns/user_dropdown.js'),
        'table_search': path.resolve(__dirname, 'assets/js/filters/table_search.js'),
        'ensure_type_work': path.resolve(__dirname, 'assets/js/forms/ensure_type_work.js'),
        'form_error_clear': path.resolve(__dirname, 'assets/js/forms/form_error_clear.js'),
        'form_navigation': path.resolve(__dirname, 'assets/js/forms/form_navigation.js'),
        'work_date_change': path.resolve(__dirname, 'assets/js/forms/work_date_change.js'),
        'duplicate_check': path.resolve(__dirname, 'assets/js/modals/duplicate_check.js'),
        'modals': path.resolve(__dirname, 'assets/js/modals/modals.js'),
        'save_confirmation': path.resolve(__dirname, 'assets/js/modals/save_confirmation.js'),  
        'navbar_toggle': path.resolve(__dirname, 'assets/js/navbar/navbar_toggle.js'),
        'summary_selected_employees': path.resolve(__dirname, 'assets/js/summary/summary_selected_employees.js'),
        'summary_selected_works': path.resolve(__dirname, 'assets/js/summary/summary_selected_works.js'),
        'theme_init': path.resolve(__dirname, 'assets/js/theme/theme_init.js'),
        'theme_switcher': path.resolve(__dirname, 'assets/js/theme/theme_switcher.js'),
        'flatpickr': path.resolve(__dirname, 'assets/src/flatpickr_init.js'),
        'styles': path.resolve(__dirname, 'assets/src/styles.css'),
      },
      output: {
        // Output JS bundles to js/ directory with -bundle suffix
        entryFileNames: `js/[name]-bundle.js`,
      },
    },
  },
});