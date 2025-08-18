import flatpickr from "flatpickr";
import "flatpickr/dist/flatpickr.min.css"; // import styles

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
});
