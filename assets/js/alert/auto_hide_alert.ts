const ALERT_SELECTORS = {
	alert: "[data-auto-hide-alert]",
} as const;

const ALERT_CLASSES = {
	hidden: "hidden",
} as const;

const ALERT_TIMEOUT = 5000 as const;

document.addEventListener("DOMContentLoaded", () => {
	for (const alert of document.querySelectorAll<HTMLElement>(
		ALERT_SELECTORS.alert,
	)) {
		setTimeout(() => {
			alert.classList.add(ALERT_CLASSES.hidden);
		}, ALERT_TIMEOUT);
	}
});
