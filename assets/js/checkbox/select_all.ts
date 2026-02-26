type CheckboxLike = HTMLInputElement;

/** Safe CSS.escape accessor without using `any` */
const cssEscape = ((): ((s: string) => string) => {
	if (
		typeof CSS !== "undefined" &&
		(CSS as unknown as { escape?: (s: string) => string }).escape
	) {
		return (CSS as unknown as { escape: (s: string) => string }).escape;
	}
	return (s: string) => s;
})();

function resolveCheckboxes(
	input: string | Iterable<CheckboxLike> | null | undefined,
): CheckboxLike[] {
	if (!input) return [];
	if (typeof input === "string") {
		const selector = `input[name="${cssEscape(input)}"]`;
		return Array.from(document.querySelectorAll<HTMLInputElement>(selector));
	}
	return Array.from(input);
}

/**
 * Toggle all visible checkboxes sharing the same name.
 * - source: checkbox element (or any object with `.checked`) that controls the group
 * - name: string name OR NodeList/Array of checkboxes
 */
export function toggleAllVisible(
	source: CheckboxLike | { checked?: boolean } | null,
	name: string | Iterable<CheckboxLike> | null | undefined,
): void {
	const checkboxList = resolveCheckboxes(name);
	if (checkboxList.length === 0) return;
	const shouldCheck = !!(source && (source as { checked?: boolean }).checked);

	if (source instanceof HTMLInputElement) {
		source.indeterminate = false;
	}

	checkboxList.forEach((cb) => {
		if (
			cb instanceof HTMLInputElement &&
			cb.type === "checkbox" &&
			cb.offsetParent !== null
		) {
			cb.checked = shouldCheck;
			cb.dispatchEvent(new Event("change", { bubbles: true }));
		}
	});
}

/* indeterminate support */
function refreshAllCheckbox(selectAll: HTMLInputElement): void {
	const name = selectAll.dataset.checkboxName;
	if (!name) return;
	const checkboxes = resolveCheckboxes(name);
	const visible = checkboxes.filter((cb) => cb.offsetParent !== null);
	const checked = visible.filter((cb) => cb.checked);

	if (checked.length === 0) {
		selectAll.checked = false;
		selectAll.indeterminate = false;
	} else if (checked.length === visible.length) {
		selectAll.checked = true;
		selectAll.indeterminate = false;
	} else {
		selectAll.checked = true;
		selectAll.indeterminate = true;
	}
}

document.addEventListener("DOMContentLoaded", () => {
	document.addEventListener("change", (e) => {
		const target = e.target as HTMLInputElement | null;
		if (!target || target.type !== "checkbox") return;

		if (target.dataset.checkboxName) {
			refreshAllCheckbox(target);
			return;
		}

		const name = target.name;
		if (name) {
			const selectAll = document.querySelector<HTMLInputElement>(
				`input[type="checkbox"][data-checkbox-name="${name}"]`,
			);
			if (selectAll) refreshAllCheckbox(selectAll);
		}
	});

	document
		.querySelectorAll<HTMLInputElement>(
			'input[type="checkbox"][data-checkbox-name]',
		)
		.forEach(refreshAllCheckbox);
});

// expose for legacy templates
declare global {
	interface Window {
		toggleAllVisible?: typeof toggleAllVisible;
	}
}
window.toggleAllVisible = toggleAllVisible;
