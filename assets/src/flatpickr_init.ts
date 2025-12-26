import "flatpickr/dist/flatpickr.min.css";
import "flatpickr/dist/plugins/monthSelect/style.css";

import flatpickr, { Instance, Options } from "flatpickr";
import monthSelectPlugin from "flatpickr/dist/plugins/monthSelect/index.js";

type MonthPluginOptions = {
  shorthand?: boolean;
  dateFormat?: string;
  altFormat?: string;
};

const createMonthPlugin = ((): ((opts: MonthPluginOptions) => unknown) => {
  // plugin may lack TS types; keep as unknown factory with strict input typing
  return monthSelectPlugin as unknown as (opts: MonthPluginOptions) => unknown;
})();

function initPicker(selector: string, options: Options): Instance[] {
  // flatpickr accepts selector string; return created instances for possible testing
  return flatpickr(selector, options) as Instance[];
}

document.addEventListener("DOMContentLoaded", () => {
  // Single Date Picker
  initPicker(".js-flatpickr", {
    dateFormat: "Y-m-d",
    allowInput: true,
    disableMobile: true,
  });

  // Range Date Picker
  initPicker(".js-flatpickr-range", {
    mode: "range",
    dateFormat: "Y-m-d",
    allowInput: true,
  });

  // Month Picker using monthSelect plugin
  initPicker(".js-flatpickr-month", {
    plugins: [createMonthPlugin({ shorthand: true, dateFormat: "Y-m", altFormat: "F Y" })] as unknown as Options["plugins"],
  });
});
