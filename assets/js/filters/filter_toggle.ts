document.addEventListener("DOMContentLoaded", () => {
	const mql = window.matchMedia("(min-width: 1024px)");

	const toggles = Array.from(
		document.querySelectorAll<HTMLButtonElement>('[data-filter-toggle="true"]'),
	);

	const applyState = (panel: HTMLElement, btn: HTMLButtonElement, open: boolean) => {
		panel.classList.toggle("hidden", !open);
		btn.setAttribute("aria-expanded", open.toString());
	};

	const applyResponsive = () => {
		toggles.forEach((btn) => {
			const targetId = btn.dataset.target;
			if (!targetId) return;
			const panel = document.getElementById(targetId);
			if (!panel) return;

			const storageKey = `filtersOpen:${targetId}`;

			if (mql.matches) {
				applyState(panel, btn, true);
				return;
			}

			const saved = sessionStorage.getItem(storageKey);
			applyState(panel, btn, saved === "true");
		});
	};

	toggles.forEach((btn) => {
		btn.addEventListener("click", () => {
			if (mql.matches) return;

			const targetId = btn.dataset.target;
			if (!targetId) return;
			const panel = document.getElementById(targetId);
			if (!panel) return;

			const isOpen = !panel.classList.contains("hidden");
			const next = !isOpen;

			applyState(panel, btn, next);
			sessionStorage.setItem(`filtersOpen:${targetId}`, next.toString());
		});
	});

	if ("addEventListener" in mql) mql.addEventListener("change", applyResponsive);
	else mql.addListener(applyResponsive);

	applyResponsive();
});
