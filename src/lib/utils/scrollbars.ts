const DEFAULT_IDLE_MS = 900;

type InitScrollbarAutohideOptions = {
	idleMs?: number;
};

export function initScrollbarAutohide(options: InitScrollbarAutohideOptions = {}) {
	if (typeof window === 'undefined') return () => {};

	const idleMs = options.idleMs ?? DEFAULT_IDLE_MS;

	const timers = new Map<HTMLElement, number>();

	const setVisible = (element: HTMLElement) => {
		element.dataset.scrollbars = 'visible';

		const existing = timers.get(element);
		if (existing !== undefined) window.clearTimeout(existing);

		const timer = window.setTimeout(() => {
			delete element.dataset.scrollbars;
			timers.delete(element);
		}, idleMs);

		timers.set(element, timer);
	};

	const resolveScrollTarget = (target: EventTarget | null): HTMLElement | null => {
		if (!target) return null;
		if (target === window || target === document) {
			const el = document.scrollingElement;
			return el instanceof HTMLElement ? el : null;
		}
		return target instanceof HTMLElement ? target : null;
	};

	const onScroll = (event: Event) => {
		const target = resolveScrollTarget(event.target);
		if (!target) return;
		setVisible(target);
	};

	window.addEventListener('scroll', onScroll, { capture: true, passive: true });

	return () => {
		window.removeEventListener('scroll', onScroll, true);
		for (const [element, timer] of timers) {
			window.clearTimeout(timer);
			delete element.dataset.scrollbars;
		}
		timers.clear();
	};
}
