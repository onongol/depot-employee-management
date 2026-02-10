// Toggles the left sidebar with overlay: opens on mobile via hamburger, closes on overlay, ESC, or retoggle.

document.addEventListener("DOMContentLoaded", () => {
	const buttons = [
		document.getElementById("sidebar-toggle") as HTMLButtonElement | null,
		document.getElementById("navbar-toggle") as HTMLButtonElement | null,
	].filter((b): b is HTMLButtonElement => b !== null);

	const sidebar = document.getElementById("app-sidebar") as HTMLElement | null;
	const overlay = document.getElementById(
		"sidebar-overlay",
	) as HTMLElement | null;
	if (!buttons.length || !sidebar || !overlay) return;

	const setAria = (open: boolean) =>
		buttons.forEach((btn) =>
			btn.setAttribute("aria-expanded", open ? "true" : "false"),
		);

	const open = () => {
		sidebar.classList.remove("-translate-x-full", "hidden");
		overlay.classList.remove("hidden");
		document.body.classList.add("overflow-hidden");
		setAria(true);
	};

	const close = () => {
		sidebar.classList.add("-translate-x-full", "hidden");
		overlay.classList.add("hidden");
		document.body.classList.remove("overflow-hidden");
		setAria(false);
	};

	buttons.forEach((btn) => {
		btn.addEventListener("click", () => {
			const openNow = btn.getAttribute("aria-expanded") === "true";
			openNow ? close() : open();
		});
	});

	overlay.addEventListener("click", () => close());

	document.addEventListener("keydown", (e: KeyboardEvent) => {
		if (e.key === "Escape") close();
	});

	// начальное состояние: закрыт на мобильном, открыт на десктопе за счёт классов Tailwind
	setAria(false);
});
