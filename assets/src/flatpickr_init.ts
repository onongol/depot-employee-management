import "flatpickr/dist/flatpickr.min.css";
import "flatpickr/dist/plugins/monthSelect/style.css";

import flatpickr from "flatpickr";
// flatpickr exposes these through a namespace, not as named exports of the package root.
import type { Instance } from "flatpickr/dist/types/instance";
import type { Options } from "flatpickr/dist/types/options";
import monthSelectPlugin from "flatpickr/dist/plugins/monthSelect/index.js";

/**
 * Options configuration for the Flatpickr Month Select plugin.
 */
type MonthPluginOptions = {
  shorthand?: boolean;
  dateFormat?: string;
  altFormat?: string;
};

/**
 * Type cast for the monthSelectPlugin to handle missing or incompatible type definitions.
 */
const createMonthPlugin = monthSelectPlugin as unknown as (
  opts: MonthPluginOptions,
) => unknown;

/**
 * Extended HTMLInputElement to store the Flatpickr instance for cleanup purposes.
 */
interface FlatpickrInput extends HTMLInputElement {
  _flatpickr?: Instance;
}

/**
 * Initializes Flatpickr instances for a given selector while ensuring
 * previous instances are destroyed to prevent memory leaks.
 * @param selector - CSS selector for the target input elements.
 * @param options - Flatpickr configuration options.
 * @returns An array of initialized Flatpickr instances.
 */
function initPicker(selector: string, options: Options): Instance[] {
  const elements = document.querySelectorAll<FlatpickrInput>(selector);
  for (const el of elements) {
    try {
      // Clean up existing Flatpickr instance if it exists
      if (el._flatpickr) {
        el._flatpickr.destroy();
      }
    } catch {
      // Ignore errors if element is already gone
    }
  }
  return flatpickr(selector, options) as Instance[];
}

/**
 * Main orchestrator to initialize all types of Flatpickr instances used in the application.
 * Handles single dates, ranges, and month-only selection.
 */
function initAllFlatpickr() {
  // Single Date Picker: Standard configuration for individual dates
  initPicker(".js-flatpickr", {
    dateFormat: "Y-m-d",
    allowInput: true,
    disableMobile: true,
  });

  // Range Date Picker: Configuration for date intervals
  initPicker(".js-flatpickr-range", {
    mode: "range",
    dateFormat: "Y-m-d",
    allowInput: true,
  });

  // Month Picker: Specialized picker using the Month Select plugin
  initPicker(".js-flatpickr-month", {
    plugins: [
      createMonthPlugin({
        shorthand: true,
        dateFormat: "Y-m",
        altFormat: "F Y",
      }),
    ] as unknown as Options["plugins"],
    disableMobile: true, // Force desktop version for better UX with the month plugin
  });
}

/**
 * Initial load binding.
 */
document.addEventListener("DOMContentLoaded", initAllFlatpickr);

/**
 * HTMX Integration: Re-initialize pickers after the DOM has been modified by HTMX.
 */
document.addEventListener("htmx:afterSwap", initAllFlatpickr);
