import { tick } from 'svelte';

type RevealExpandedSectionOptions = {
	offset?: number;
	followDuration?: number;
};

const SCROLLABLE_OVERFLOW_PATTERN = /(auto|scroll|overlay)/;

const nextAnimationFrame = () =>
	new Promise<number>((resolve) => {
		requestAnimationFrame(resolve);
	});

const clamp = (value: number, min: number, max: number) => Math.min(max, Math.max(min, value));

const isScrollableY = (element: HTMLElement) => {
	const { overflowY } = getComputedStyle(element);
	return SCROLLABLE_OVERFLOW_PATTERN.test(overflowY);
};

const findScrollContainer = (sectionEl: HTMLElement) => {
	let fallback: HTMLElement | null = null;
	let parent = sectionEl.parentElement;

	while (parent) {
		if (isScrollableY(parent)) {
			fallback ??= parent;
			if (parent.scrollHeight > parent.clientHeight + 1) {
				return parent;
			}
		}

		parent = parent.parentElement;
	}

	if (fallback) {
		return fallback;
	}

	const settingsContainer = document.getElementById('settings-container');
	if (settingsContainer instanceof HTMLElement) {
		return settingsContainer;
	}

	return document.scrollingElement instanceof HTMLElement ? document.scrollingElement : null;
};

const getAlignedScrollState = (container: HTMLElement, sectionEl: HTMLElement, offset: number) => {
	const containerRect = container.getBoundingClientRect();
	const sectionRect = sectionEl.getBoundingClientRect();
	const maxScrollTop = Math.max(0, container.scrollHeight - container.clientHeight);
	const desiredScrollTop = container.scrollTop + sectionRect.top - containerRect.top - offset;

	return {
		desiredScrollTop,
		nextScrollTop: clamp(desiredScrollTop, 0, maxScrollTop),
		maxScrollTop
	};
};

export const revealExpandedSection = async (
	sectionEl: HTMLElement | null | undefined,
	{ offset = 8, followDuration = 220 }: RevealExpandedSectionOptions = {}
) => {
	if (!sectionEl || typeof window === 'undefined') {
		return;
	}

	await tick();
	await nextAnimationFrame();

	const container = findScrollContainer(sectionEl);
	if (!container) {
		sectionEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
		return;
	}

	const restoreOverflowAnchor = container.style.overflowAnchor;
	container.style.overflowAnchor = 'none';

	try {
		let state = getAlignedScrollState(container, sectionEl, offset);
		const isBottomLimited =
			state.desiredScrollTop > state.maxScrollTop + 1 &&
			Math.abs(container.scrollTop - state.maxScrollTop) < 1;

		if (!isBottomLimited) {
			if (Math.abs(container.scrollTop - state.nextScrollTop) > 1) {
				container.scrollTo({ top: state.nextScrollTop, behavior: 'smooth' });
			}
			return;
		}

		const endTime = performance.now() + followDuration;
		while (performance.now() < endTime) {
			await nextAnimationFrame();
			state = getAlignedScrollState(container, sectionEl, offset);
			if (Math.abs(container.scrollTop - state.nextScrollTop) > 0.5) {
				container.scrollTop = state.nextScrollTop;
			}
		}

		state = getAlignedScrollState(container, sectionEl, offset);
		if (Math.abs(container.scrollTop - state.nextScrollTop) > 0.5) {
			container.scrollTop = state.nextScrollTop;
		}
	} finally {
		await nextAnimationFrame();
		container.style.overflowAnchor = restoreOverflowAnchor;
	}
};
