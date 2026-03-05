document.addEventListener("DOMContentLoaded", () => {
	const syncRowMeta = (cb: HTMLInputElement): void => {
		const row = cb.closest("tr");
		if (!row) return;

		const meta = row.querySelector<HTMLElement>("[data-mobile-meta]");
		if (!meta) return;

		if (cb.checked) {
			meta.classList.remove("grid-rows-[0fr]");
			meta.classList.add("grid-rows-[1fr]");
		} else {
			meta.classList.remove("grid-rows-[1fr]");
			meta.classList.add("grid-rows-[0fr]");
		}
	};

	document
		.querySelectorAll<HTMLInputElement>('input[name="work_ids"], input[name="employee_ids"], input[name="daily_work_ids"], input[name="daily_salary_ids"]')
		.forEach((cb) => syncRowMeta(cb));

	document.addEventListener("change", (e: Event) => {
		const target = e.target;
		if (!(target instanceof HTMLInputElement)) return;
		if (
			target.name === "work_ids" ||
			target.name === "employee_ids" ||
			target.name === "daily_work_ids" ||
			target.name === "daily_salary_ids"
		) {
			syncRowMeta(target);
		}
	});
});
