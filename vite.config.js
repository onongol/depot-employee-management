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
        'auto_hide_alert': path.resolve(__dirname, 'assets/js/alert/auto_hide_alert.ts'),
        'amount_inputs': path.resolve(__dirname, 'assets/js/amount/amount_inputs.ts'),
        'amount_validation': path.resolve(__dirname, 'assets/js/amount/amount_validation.ts'),
        'password_toggle': path.resolve(__dirname, 'assets/js/auth/password_toggle.ts'),
        'bulk_delete_toggle': path.resolve(__dirname, 'assets/js/buttons/bulk_delete_toggle.ts'),
        'checkbox_validation': path.resolve(__dirname, 'assets/js/checkbox/checkbox_validation.ts'),
        'mobile_select_details': path.resolve(__dirname, 'assets/js/checkbox/mobile_select_details.ts'),
        'select_all': path.resolve(__dirname, 'assets/js/checkbox/select_all.ts'),
        'department_dropdown': path.resolve(__dirname, 'assets/js/dropdowns/department_dropdown.ts'),
        'user_dropdown': path.resolve(__dirname, 'assets/js/dropdowns/user_dropdown.ts'),
        'filter_toggle': path.resolve(__dirname, 'assets/js/filters/filter_toggle.ts'),
        'table_search': path.resolve(__dirname, 'assets/js/filters/table_search.ts'),
        'ensure_type_work': path.resolve(__dirname, 'assets/js/forms/ensure_type_work.ts'),
        'form_error_clear': path.resolve(__dirname, 'assets/js/forms/form_error_clear.ts'),
        'form_navigation': path.resolve(__dirname, 'assets/js/forms/form_navigation.ts'),
        'step_navigation': path.resolve(__dirname, 'assets/js/forms/step_navigation.ts'),
        'work_date_change': path.resolve(__dirname, 'assets/js/forms/work_date_change.ts'),
        'duplicate_check': path.resolve(__dirname, 'assets/js/modals/duplicate_check.ts'),
        'modals': path.resolve(__dirname, 'assets/js/modals/modals.ts'),
        'save_confirmation': path.resolve(__dirname, 'assets/js/modals/save_confirmation.ts'),
        'sidebar_toggle': path.resolve(__dirname, 'assets/js/sidebar/sidebar_toggle.ts'),  
        'summary_selected': path.resolve(__dirname, 'assets/js/summary/summary_selected.ts'),
        'theme_init': path.resolve(__dirname, 'assets/js/theme/theme_init.ts'),
        'theme_switcher': path.resolve(__dirname, 'assets/js/theme/theme_switcher.ts'),
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