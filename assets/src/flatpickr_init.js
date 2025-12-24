import "flatpickr/dist/flatpickr.min.css";
import "flatpickr/dist/themes/dark.css";
import "flatpickr/dist/plugins/monthSelect/style.css";

import flatpickr from "flatpickr";
import monthSelectPlugin from "flatpickr/dist/plugins/monthSelect/index.js";


document.addEventListener('DOMContentLoaded', function () {
  // Single Date Picker
  flatpickr(".js-flatpickr", {
    dateFormat: "Y-m-d",
    allowInput: true,
    disableMobile: true, 
    //locale: Mongolian
  });
  // Range Date Picker
  flatpickr(".js-flatpickr-range", {
    mode: "range",
    dateFormat: "Y-m-d",
    allowInput: true,
  });
  // Month Picker
  flatpickr(".js-flatpickr-month", {
    plugins: [new monthSelectPlugin({
      shorthand: true,
      dateFormat: "Y-m",
      altFormat: "F Y"
    })]
  });
});
