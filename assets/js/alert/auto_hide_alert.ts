const ALERT_HIDE_SELECTORS = {
	alert: "[data-auto-hide-alert]",
} as const;

const ALERT_HIDE_CLASSES = {
	hidden: "hidden",
} as const;

const ALERT_HIDE_TIMEOUT = 5000 as const;

document.addEventListener("DOMContentLoaded", () => {
	for (const alert of document.querySelectorAll<HTMLElement>(
		ALERT_HIDE_SELECTORS.alert,
	)) {
		setTimeout(() => {
			alert.classList.add(ALERT_HIDE_CLASSES.hidden);
		}, ALERT_HIDE_TIMEOUT);
	}
});
