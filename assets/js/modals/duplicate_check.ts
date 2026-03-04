/**
 * Prevent duplicate piecework entries on create:
 * - strict types, no `any`
 * - safer DOM access and early returns
 * - normalized wagon comparison and resilient JSON parsing
 */

type ExistingPiecework = {
	employee_id: number | string;
	work_id: number | string;
	type_work: string;
	work_date: string;
	wagon_number?: string | null;
};

document.addEventListener("DOMContentLoaded", () => {
	const existingPieceworksEl = document.getElementById(
		"existing-pieceworks",
	) as HTMLScriptElement | null;
	const existingPieceworks: ExistingPiecework[] = (() => {
		if (!existingPieceworksEl || !existingPieceworksEl.textContent) return [];
		try {
			return JSON.parse(
				existingPieceworksEl.textContent,
			) as ExistingPiecework[];
		} catch {
			return [];
		}
	})();

	const form = document.getElementById("createForm") as HTMLFormElement | null;
	if (!form) return;

	const modalDiv = document.getElementById(
		"saveDuplicateModal",
	) as HTMLElement | null;
	const confirmBtn = document.getElementById(
		"confirmSaveBtn",
	) as HTMLButtonElement | null;
	const cancelBtn = document.querySelector(
		"#saveDuplicateModal [data-modal-cancel]",
	) as HTMLElement | null;
	let allowSubmit = false;

	const openModal = (modal: HTMLElement) => {
		modal.classList.remove("hidden");
		document.body.classList.add("overflow-hidden");
	};

	const closeModal = (modal: HTMLElement) => {
		modal.classList.add("hidden");
		document.body.classList.remove("overflow-hidden");
	};

	const normalizeWagon = (val: unknown): string | null => {
		if (val === null || val === undefined) return null;
		const s = String(val).trim();
		return s === "" ? null : s;
	};

	form.addEventListener("submit", (e) => {
		if (allowSubmit) {
			allowSubmit = false;
			return;
		}

		// Skip duplicate check when amount validation already shows error
		if (document.getElementById("amount-error")) return;

		// Collect selections
		const selectedEmployeeIds = Array.from(
			document.querySelectorAll<HTMLInputElement>(
				'input[name="employee_ids"]:checked',
			),
		).map((cb) => cb.value);
		const selectedWorkIds = Array.from(
			document.querySelectorAll<HTMLInputElement>(
				'input[name="work_ids"]:checked',
			),
		).map((cb) => cb.value);

		const typeWorkEl = document.getElementById("type_work") as
			| HTMLSelectElement
			| HTMLInputElement
			| null;
		const workDateEl = document.getElementById(
			"work_date",
		) as HTMLInputElement | null;
		const wagonNumberInput = document.getElementById(
			"wagon_number",
		) as HTMLInputElement | null;

		const typeWork = typeWorkEl?.value ?? "";
		const workDate = workDateEl?.value ?? "";
		const wagonNumber = normalizeWagon(wagonNumberInput?.value);

		if (selectedEmployeeIds.length === 0 || selectedWorkIds.length === 0)
			return;

		// Check duplicates + collect matched pairs
		const duplicatePairs: Array<{ empId: string; workId: string }> = [];

		selectedEmployeeIds.forEach((empId) => {
			selectedWorkIds.forEach((workId) => {
				const exists = existingPieceworks.some(
					(pw) =>
						String(pw.employee_id) === String(empId) &&
						String(pw.work_id) === String(workId) &&
						pw.type_work === typeWork &&
						pw.work_date === workDate &&
						normalizeWagon(pw.wagon_number) === wagonNumber,
				);
				if (exists)
					duplicatePairs.push({ empId: String(empId), workId: String(workId) });
			});
		});

		if (duplicatePairs.length === 0) return;

		// Prevent submit and show modal
		e.preventDefault();
		if (!modalDiv) return;

		const duplicateEmpIds = new Set(duplicatePairs.map((p) => p.empId));
		const duplicateWorkIds = new Set(duplicatePairs.map((p) => p.workId));

		const selectedEmployees = Array.from(
			document.querySelectorAll<HTMLInputElement>(
				'input[name="employee_ids"]:checked',
			),
		)
			.filter((cb) => duplicateEmpIds.has(String(cb.value)))
			.map((cb) => {
				const tr = cb.closest("tr");
				const id = (tr?.getAttribute("data-emp-id") ?? cb.value ?? "").trim();
				const name = (tr?.getAttribute("data-emp-name") ?? "").trim();
				return name ? `(ID: ${id}) ${name}` : id;
			});

		const selectedWorks = Array.from(
			new Set(
				Array.from(
					document.querySelectorAll<HTMLInputElement>(
						'input[name="work_ids"]:checked',
					),
				)
					.filter((cb) => duplicateWorkIds.has(String(cb.value)))
					.map((cb) => {
						const tr = cb.closest("tr");
						return (
							cb.dataset.workName?.trim() ||
							tr?.getAttribute("data-work-name")?.trim() ||
							""
						);
					})
					.filter(Boolean),
			),
		);

		const setText = (id: string, text: string) => {
			const el = document.getElementById(id);
			if (el) el.textContent = text;
		};

		setText("modal-employee", selectedEmployees.join(", "));
		setText("modal-work", selectedWorks.join(", "));
		setText("modal-type-work", typeWork);
		setText("modal-wagon-number", wagonNumber ?? "-");
		setText("modal-work-date", workDate);

		openModal(modalDiv);
	});

	if (confirmBtn && form && modalDiv) {
		confirmBtn.addEventListener("click", (evt) => {
			evt.preventDefault();
			allowSubmit = true;
			closeModal(modalDiv);
			form.requestSubmit();
		});
	}

	if (cancelBtn && modalDiv) {
		cancelBtn.addEventListener("click", (evt) => {
			evt.preventDefault();
			closeModal(modalDiv);
		});
	}

	// Close modal on Escape
	document.addEventListener("keydown", (evt: KeyboardEvent) => {
		if (evt.key !== "Escape" || !modalDiv) return;
		if (!modalDiv.classList.contains("hidden")) closeModal(modalDiv);
	});
});
