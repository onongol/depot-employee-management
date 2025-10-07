import flatpickr from "flatpickr";
//import "flatpickr/dist/flatpickr.min.css"; // import styles
import monthSelectPlugin from "flatpickr/dist/plugins/monthSelect/index.js";

document.addEventListener('DOMContentLoaded', function () {
  // Single Date Picker
  flatpickr(".js-flatpickr", {
    dateFormat: "Y-m-d",
    allowInput: true,
    //locale: Mongolian
  });
  // Range Date Picker
  flatpickr(".js-flatpickr-range", {
    mode: "range",
    dateFormat: "Y-m-d",
    allowInput: true
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


