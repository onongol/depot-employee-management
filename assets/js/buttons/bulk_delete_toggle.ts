document.addEventListener("DOMContentLoaded", () => {
	const btn = document.getElementById("bulk-delete-button");
	if (!btn) return;

	// support both daily_salary and daily_work checkboxes
	const selectors = [
		'input[name="daily_salary_ids"]',
		'input[name="daily_work_ids"]',
	];

	// {changed code}
	const checkedSelector = selectors.map(s => `${s}:checked`).join(", ");

	const toggle = () => {
		const any = Boolean(document.querySelector(checkedSelector));
		btn.classList.toggle("hidden", !any);
		btn.classList.toggle("flex", any);
	};

	document.addEventListener("change", (e: Event) => {
		const target = e.target;
		if (!(target instanceof HTMLInputElement)) return;
		if (
			selectors.includes(`input[name="${target.name}"]`) ||
			/select-all/i.test(target.id || "")
		)
			toggle();
	});

	toggle();
});
