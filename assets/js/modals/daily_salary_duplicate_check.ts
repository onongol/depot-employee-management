import {
  DUPLICATE_TAGS,
  type ExistingDailySalary,
  formatEmployeeDisplay,
  getDuplicateById,
  openDuplicateModal,
  parseJsonScript,
  setDuplicateText,
  setupDuplicateModalClose,
} from "./duplicate_check";

const DS_DUPLICATE_SELECTORS = {
  existingScript: "existing-daily-salaries",
  form: "createForm",
  modal: "saveDuplicateModal",
  modalCancel: "[data-modal-cancel]",
  employeeCheckbox: 'input[name="employee_ids"]:checked',
  salaryDate: "salary_date",
} as const;

const DS_DUPLICATE_ATTRS = {
  empId: "data-emp-id",
  empName: "data-emp-name",
} as const;

const DS_DUPLICATE_ELEMENTS = {
  detailEmployee: "duplicateDetailEmployee",
  detailSalaryDate: "duplicateDetailSalaryDate",
} as const;

/**
 * Creates a unique key
 */
function makeDuplicateKey(keyEmpId: string, keySalaryDate: string): string {
  return `${keyEmpId}::${keySalaryDate}`;
}

/**
 * Generates a unique key
 */
function makeDuplicateKeyFrom(ds: ExistingDailySalary): string {
  return makeDuplicateKey(String(ds.employee_code), ds.salary_date);
}

/* Initialization */
document.addEventListener("DOMContentLoaded", () => {
  const existing = parseJsonScript<ExistingDailySalary>(
    DS_DUPLICATE_SELECTORS.existingScript,
  );
  const existingSet = new Set(existing.map(makeDuplicateKeyFrom));
  const form = getDuplicateById(
    DS_DUPLICATE_SELECTORS.form,
  ) as HTMLFormElement | null;
  const modalDiv = getDuplicateById(DS_DUPLICATE_SELECTORS.modal);

  if (!form || !modalDiv) return;

  setupDuplicateModalClose(modalDiv, DS_DUPLICATE_SELECTORS.modalCancel);

  /**
   * Core validation logic triggered on form submission.
   */
  form.addEventListener("submit", (event) => {
    // Gather selected employee IDs from the form checkboxes
    const employeeCheckboxes = Array.from(
      document.querySelectorAll<HTMLInputElement>(
        DS_DUPLICATE_SELECTORS.employeeCheckbox,
      ),
    );

    const salaryDateEl = getDuplicateById(
      DS_DUPLICATE_SELECTORS.salaryDate,
    ) as HTMLInputElement | null;

    // Stop check if salary date is missing or no employees are selected (prevents false duplicate errors)
    if (!salaryDateEl || employeeCheckboxes.length === 0) return;

    const salaryDate = salaryDateEl.value;

    // Check if any selected employee/salary date combination already exists
    const duplicates = employeeCheckboxes.filter((checkbox) =>
      existingSet.has(makeDuplicateKey(checkbox.value, salaryDate)),
    );

    // Proceed with standard submission if no duplicates were found
    if (duplicates.length === 0) return;

    // Duplicates found: Prevent submission and prepare modal data
    event.preventDefault();

    const selectedEmployees = duplicates.map((checkbox) => {
      const tr = checkbox.closest(DUPLICATE_TAGS.tableRow);
      const id = (
        tr?.getAttribute(DS_DUPLICATE_ATTRS.empId) ?? checkbox.value
      ).trim();
      const name = (tr?.getAttribute(DS_DUPLICATE_ATTRS.empName) ?? "").trim();
      return formatEmployeeDisplay(id, name);
    });

    setDuplicateText(
      DS_DUPLICATE_ELEMENTS.detailEmployee,
      selectedEmployees.join(", "),
    );
    setDuplicateText(DS_DUPLICATE_ELEMENTS.detailSalaryDate, salaryDate);

    openDuplicateModal(modalDiv);
  });
});
