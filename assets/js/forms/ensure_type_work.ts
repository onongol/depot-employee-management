// Ensures all select[name="type_work"] elements have id="type_work" for compatibility with other scripts that expect this ID.

type VoidFn = () => void;

const ensureTypeWork: VoidFn = () => {
  const selects = document.querySelectorAll<HTMLSelectElement>('select[name="type_work"]');
  if (selects.length === 0) return;

  // If an element with the canonical id already exists, prefer it (avoid duplicate IDs).
  if (document.getElementById('type_work')) return;

  const first = selects[0];
  first.id = 'type_work';
};

document.addEventListener('DOMContentLoaded', ensureTypeWork);