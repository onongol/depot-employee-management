document.addEventListener("DOMContentLoaded", () => {
	const mql = window.matchMedia("(min-width: 1024px)");
	const toggles = Array.from(
		document.querySelectorAll<HTMLButtonElement>('[data-filter-toggle="true"]'),
	);
	const overlays = new Map<string, HTMLElement>();
	document
		.querySelectorAll<HTMLElement>("[data-filter-overlay]")
		.forEach((o) => overlays.set(o.dataset.filterOverlay ?? "", o));

	const applyState = (
		panel: HTMLElement,
		btn: HTMLButtonElement,
		open: boolean,
	) => {
		const overlay = overlays.get(panel.id);
		const isDesktop = mql.matches;

		// overlay & body lock только на мобилке
		if (overlay) overlay.classList.toggle("hidden", isDesktop || !open);
		document.body.classList.toggle(
			"overflow-hidden",
			!isDesktop && open && !!overlay,
		);

		// панель
		panel.classList.toggle("hidden", isDesktop ? false : !open);
		panel.classList.toggle("translate-y-full", isDesktop ? false : !open);
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

			const isOpen = !panel.classList.contains("translate-y-full") && !panel.classList.contains("hidden");
			const next = !isOpen;

			applyState(panel, btn, next);
			sessionStorage.setItem(`filtersOpen:${targetId}`, next.toString());
		});
	});

	// закрытие по клику на оверлей (только мобилка)
	document
		.querySelectorAll<HTMLElement>("[data-filter-overlay]")
		.forEach((overlay) => {
			overlay.addEventListener("click", () => {
				const targetId = overlay.dataset.filterOverlay;
				if (!targetId) return;
				const panel = document.getElementById(targetId);
				const btn = toggles.find((b) => b.dataset.target === targetId);
				if (!panel || !btn) return;
				applyState(panel, btn, false);
				sessionStorage.setItem(`filtersOpen:${targetId}`, "false");
			});
		});

	if ("addEventListener" in mql) mql.addEventListener("change", applyResponsive);
	else mql.addListener(applyResponsive);

	applyResponsive();
});
