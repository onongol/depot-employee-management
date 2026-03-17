/**
 * Safe JSON parsing for script-tag based data injection (useful for localized strings)
 */
export function readJsonScript(id: string): string {
	const el = document.getElementById(id);
	if (!el) return "";
	try {
		return JSON.parse(el.textContent ?? '""') as string;
	} catch {
		return "";
	}
}
