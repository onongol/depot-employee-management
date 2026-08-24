/**
 * Interface representing the core elements of a dropdown component.
 */
interface DropdownElements {
  button: HTMLButtonElement;
  menu: HTMLElement;
}

// Configuration constants for DOM selectors, CSS classes, and key codes.
const DROPDOWN_SELECTORS = {
  dropdownRoot: "[data-dropdown]",
  dropdownButton: "[data-dropdown-button]",
  dropdownMenu: "[data-dropdown-menu]",
  dropdownItems: "a,button",
  panelTrigger: "[data-open-panel]",
  panels: "[data-panel]",
} as const;

const DROPDOWN_CLASSES = {
  hidden: "hidden",
} as const;

const DROPDOWN_KEYS = {
  escape: "Escape",
} as const;

const DROPDOWN_PANELS = {
  main: "main",
  language: "language",
  theme: "theme",
} as const;

type PanelName = (typeof DROPDOWN_PANELS)[keyof typeof DROPDOWN_PANELS];

document.addEventListener("DOMContentLoaded", () => {
  // Keep track of currently active (visible) menus.
  const openMenus = new Set<HTMLElement>();

  // Shows a specific dropdown menu and tracks it.
  const openMenu = (menu: HTMLElement): void => {
    menu.classList.remove(DROPDOWN_CLASSES.hidden);
    openMenus.add(menu);
  };

  // Hides a specific dropdown menu and updates tracking.
  const closeMenu = (menu: HTMLElement): void => {
    menu.classList.add(DROPDOWN_CLASSES.hidden);
    openMenus.delete(menu);
  };

  // Closes all currently open dropdown menus.
  const closeAllMenus = (): void => {
    [...openMenus].forEach(closeMenu);
  };

  /**
   * Finds and validates required dropdown elements within a root container.
   */
  function getDropdownElements(root: HTMLElement): DropdownElements | null {
    const button = root.querySelector<HTMLButtonElement>(
      DROPDOWN_SELECTORS.dropdownButton,
    );
    const menu = root.querySelector<HTMLElement>(
      DROPDOWN_SELECTORS.dropdownMenu,
    );
    if (!button || !menu) return null;
    return { button, menu };
  }

  /**
   * Shows the specified panel within the dropdown menu and hides others.
   */
  function setActivePanel(menu: HTMLElement, panelName: PanelName): void {
    menu
      .querySelectorAll<HTMLElement>(DROPDOWN_SELECTORS.panels)
      .forEach((panel) => {
        panel.classList.toggle(
          DROPDOWN_CLASSES.hidden,
          panel.dataset.panel !== panelName,
        );
      });
  }

  /**
   * Initializes logic and event listeners for a single dropdown instance.
   */
  function setupDropdown(root: HTMLElement): void {
    const elements = getDropdownElements(root);
    if (!elements) return;

    const { button, menu } = elements;

    button.addEventListener("click", (e: MouseEvent) => {
      e.stopPropagation();
      if (menu.classList.contains(DROPDOWN_CLASSES.hidden)) {
        setActivePanel(menu, DROPDOWN_PANELS.main);
        openMenu(menu);
      } else {
        closeMenu(menu);
      }
    });

    menu.addEventListener("click", (e: MouseEvent) => e.stopPropagation());

    // Close menu when any item (except panel triggers) is clicked.
    menu
      .querySelectorAll<HTMLElement>(DROPDOWN_SELECTORS.dropdownItems)
      .forEach((item) => {
        if (item.matches(DROPDOWN_SELECTORS.panelTrigger)) return;
        item.addEventListener("click", () => closeMenu(menu));
      });

    // Switch panels: main/language/theme
    menu
      .querySelectorAll<HTMLElement>(DROPDOWN_SELECTORS.panelTrigger)
      .forEach((trigger) => {
        trigger.addEventListener("click", (e: MouseEvent) => {
          e.preventDefault();
          e.stopPropagation();
          const target = trigger.dataset.openPanel as PanelName | undefined;
          if (!target || !Object.values(DROPDOWN_PANELS).includes(target))
            return;

          setActivePanel(menu, target);
        });
      });
  }

  // Initialize all dropdowns found on the page.
  document
    .querySelectorAll<HTMLElement>(DROPDOWN_SELECTORS.dropdownRoot)
    .forEach(setupDropdown);

  // Global handlers to close menus on outside click or Escape key press.
  document.addEventListener("click", closeAllMenus);
  document.addEventListener("keydown", (e: KeyboardEvent) => {
    if (e.key === DROPDOWN_KEYS.escape) closeAllMenus();
  });
});
