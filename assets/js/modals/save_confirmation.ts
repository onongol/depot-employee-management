// Shows a confirmation modal before saving: opens modal on Save click, prevents page scroll, submits the form on confirm, and closes modal on Escape or Cancel.

document.addEventListener("DOMContentLoaded", () => {
	const saveBtn = document.getElementById(
		"saveButton",
	) as HTMLButtonElement | null;
	const saveModal = document.getElementById("saveModal") as HTMLElement | null;
	const confirmBtn = document.getElementById(
		"confirmSaveButton",
	) as HTMLButtonElement | null;
	const updateForm = document.getElementById(
		"updateForm",
	) as HTMLFormElement | null;

	const isModalOpen = (): boolean =>
		!!saveModal && !saveModal.classList.contains("hidden");

	const closeSaveModal = (): void => {
		if (!saveModal) return;
		saveModal.classList.add("hidden");
		document.body.classList.remove("overflow-hidden");
	};

	if (saveBtn && saveModal) {
		saveBtn.addEventListener("click", (e: MouseEvent) => {
			e.preventDefault();
			saveModal.classList.remove("hidden");
			document.body.classList.add("overflow-hidden");
		});
	}

	if (confirmBtn && updateForm) {
		confirmBtn.addEventListener("click", (e: MouseEvent) => {
			e.preventDefault();
			// prefer requestSubmit for proper form handling
			if (
				typeof (updateForm as HTMLFormElement & { requestSubmit?: Function })
					.requestSubmit === "function"
			) {
				(
					updateForm as HTMLFormElement & { requestSubmit?: Function }
				).requestSubmit();
			} else {
				updateForm.submit();
			}
			closeSaveModal();
		});
	}

	if (saveModal) {
		const onKeydown = (e: KeyboardEvent): void => {
			if (e.key === "Escape" && isModalOpen()) closeSaveModal();
		};
		document.addEventListener("keydown", onKeydown);

		document
			.querySelectorAll<HTMLElement>("[data-modal-cancel]")
			.forEach((btn) => {
				btn.addEventListener("click", (e: Event) => {
					e.preventDefault();
					closeSaveModal();
				});
			});
	}
});
