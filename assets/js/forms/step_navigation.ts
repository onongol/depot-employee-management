document.addEventListener("DOMContentLoaded", () => {
  const step1 = document.getElementById("step-1");
  const step2 = document.getElementById("step-2");
  const nextBtn = document.getElementById("btn-step1-next");
  const backBtn = document.getElementById("btn-step2-back");
  const mobileBackBtn = document.getElementById("mobile-btn-step2-back");
  const form = document.getElementById("createForm");

  const setStep = (step: 1 | 2) => {
    if (!step1 || !step2) return;

    if (step === 1) {
      step1.classList.remove("hidden");
      step2.classList.add("hidden");
      mobileBackBtn?.classList.add("hidden");
    } else {
      step1.classList.add("hidden");
      step2.classList.remove("hidden");
      mobileBackBtn?.classList.remove("hidden");
    }
  };

  const validationEl = document.querySelector(
    '[data-checkbox-validation="true"][data-checkbox-name="employee_ids"]'
  );
  const tableSelector =
    validationEl?.getAttribute("data-table-selector") || ".employee-table-container";
  const errorMessage =
    validationEl?.getAttribute("data-error-message") || "Select at least one employee.";
  const errorId = "employee_ids-selection-error";

  const showSelectionError = (tableDiv: Element | null) => {
    if (!tableDiv) return;
    tableDiv.classList.add("border-red-500", "dark:border-red-500");
    let errorDiv = document.getElementById(errorId);
    if (!errorDiv) {
      errorDiv = document.createElement("div");
      errorDiv.id = errorId;
      errorDiv.className = "text-red-500 text-sm";
      errorDiv.textContent = errorMessage;
      const parent = tableDiv.parentNode;
      if (parent) parent.insertBefore(errorDiv, tableDiv.nextSibling);
    }
  };

  const hideSelectionError = (tableDiv: Element | null) => {
    if (!tableDiv) return;
    tableDiv.classList.remove("border-red-500", "dark:border-red-500");
    const errorDiv = document.getElementById(errorId);
    if (errorDiv) errorDiv.remove();
  };

  if (step1 && step2 && nextBtn) {
    nextBtn.addEventListener("click", () => {
      const checked = form?.querySelectorAll("input[name=\"employee_ids\"]:checked") || [];
      const tableDiv = form?.querySelector(tableSelector) ?? document.querySelector(tableSelector);
      if (checked.length === 0) {
        showSelectionError(tableDiv);
        return;
      }
      hideSelectionError(tableDiv);
      setStep(2);
      step2.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  }

  if (step1 && step2 && backBtn) {
    backBtn.addEventListener("click", () => {
      setStep(1);
      step1.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  }

  if (step1 && step2 && mobileBackBtn) {
    mobileBackBtn.addEventListener("click", () => {
      setStep(1);
      step1.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  }

  setStep(1); // initial state
});