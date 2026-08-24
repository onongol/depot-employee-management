/**
 * Sidebar Toggle Logic:
 * Manages a responsive sidebar with an overlay.
 * Features: Toggle via buttons, Close via Overlay/ESC, and Viewport synchronization.
 */
const SIDEBAR_IDS = {
  sidebar: "app-sidebar",
  overlay: "sidebar-overlay",
} as const;

const SIDEBAR_CLASSES = {
  hidden: "hidden",
  translateClosed: "-translate-x-full",
  bodyLock: "overflow-hidden",
} as const;

const SIDEBAR_KEYS = {
  escape: "Escape",
} as const;

// Media query string matching Tailwind's 'lg' breakpoint (1024px)
const SIDEBAR_MEDIA = {
  desktop: "(min-width: 1024px)",
} as const;

const SIDEBAR_SELECTORS = {
  toggleButtons: "[data-sidebar-toggle]",
} as const;

const SIDEBAR_ATTRS = {
  ariaExpanded: "aria-expanded",
} as const;

document.addEventListener("DOMContentLoaded", () => {
  // Collect all trigger buttons (e.g., hamburger menu and close button)
  const buttons = Array.from(
    document.querySelectorAll<HTMLButtonElement>(
      SIDEBAR_SELECTORS.toggleButtons,
    ),
  );

  const sidebar = document.getElementById(SIDEBAR_IDS.sidebar);
  const overlay = document.getElementById(SIDEBAR_IDS.overlay);

  // Guard clause to ensure required DOM elements exist
  if (
    !buttons.length ||
    !(sidebar instanceof HTMLElement) ||
    !(overlay instanceof HTMLElement)
  )
    return;

  // Local state tracking for the sidebar visibility
  let isSidebarOpen = false;

  /**
   * Updates Accessibility (A11y) attributes for all registered toggle buttons.
   */
  const setAriaExpanded = (open: boolean): void => {
    buttons.forEach((btn) => {
      btn.setAttribute(SIDEBAR_ATTRS.ariaExpanded, String(open));
    });
  };

  /**
   * Orchestrates the sidebar state by toggling CSS classes and ARIA attributes.
   */
  const applySidebarState = (open: boolean): void => {
    isSidebarOpen = open;

    // Toggle visibility classes
    sidebar.classList.toggle(SIDEBAR_CLASSES.translateClosed, !open);

    // Prevent/restore body scrolling
    overlay.classList.toggle(SIDEBAR_CLASSES.hidden, !open);
    document.body.classList.toggle(SIDEBAR_CLASSES.bodyLock, open);

    setAriaExpanded(open);
  };

  const open = (): void => {
    applySidebarState(true);
  };

  const close = (): void => {
    applySidebarState(false);
  };

  /**
   * Toggles sidebar state, restricted to mobile/tablet viewports.
   */
  const toggle = (): void => {
    if (desktopMql.matches) return;
    if (isSidebarOpen) close();
    else open();
  };

  // Initialize Media Query Listener for responsive synchronization
  const desktopMql = window.matchMedia(SIDEBAR_MEDIA.desktop);

  /**
   * Automatically closes mobile sidebar states when transitioning to desktop view.
   */
  const syncWithViewport = (): void => {
    if (desktopMql.matches) {
      // Force-close mobile states on desktop breakpoint
      applySidebarState(false);
      return;
    }

    // Ensure sidebar is in its correct initial state for mobile
    if (!isSidebarOpen) {
      sidebar.classList.add(SIDEBAR_CLASSES.translateClosed);
      overlay.classList.add(SIDEBAR_CLASSES.hidden);
    }
  };

  // Event Listeners initialization
  buttons.forEach((btn) => {
    btn.addEventListener("click", toggle);
  });

  overlay.addEventListener("click", close);

  // Allow closing the sidebar with the Escape key for better UX
  document.addEventListener("keydown", (e: KeyboardEvent) => {
    if (e.key === SIDEBAR_KEYS.escape) close();
  });

  // Listen for screen size changes (Desktop <-> Mobile)
  desktopMql.addEventListener("change", syncWithViewport);

  // Initial sync on page load
  syncWithViewport();
});
