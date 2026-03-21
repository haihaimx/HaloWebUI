<script lang="ts">
	import { onMount, onDestroy, getContext } from 'svelte';
	import type { Writable } from 'svelte/store';
	import type { i18n as i18nType } from 'i18next';
	import { WEBUI_API_BASE_URL } from '$lib/constants';

	const i18n = getContext<Writable<i18nType>>('i18n');

	let terminalContainer: HTMLDivElement;
	let terminal: any;
	let fitAddon: any;
	let ws: WebSocket | null = null;
	let connected = false;

	async function initTerminal() {
		const { Terminal } = await import('@xterm/xterm');
		const { FitAddon } = await import('@xterm/addon-fit');

		terminal = new Terminal({
			cursorBlink: true,
			fontSize: 14,
			fontFamily: 'Menlo, Monaco, Consolas, "Courier New", monospace',
			theme: {
				background: '#1a1b26',
				foreground: '#c0caf5',
				cursor: '#c0caf5',
				selectionBackground: '#33467c',
				black: '#15161e',
				red: '#f7768e',
				green: '#9ece6a',
				yellow: '#e0af68',
				blue: '#7aa2f7',
				magenta: '#bb9af7',
				cyan: '#7dcfff',
				white: '#a9b1d6'
			}
		});

		fitAddon = new FitAddon();
		terminal.loadAddon(fitAddon);
		terminal.open(terminalContainer);
		fitAddon.fit();

		// Connect WebSocket
		connect();

		// Handle terminal input
		terminal.onData((data: string) => {
			if (ws?.readyState === WebSocket.OPEN) {
				ws.send(data);
			}
		});

		// Handle resize
		terminal.onResize(({ cols, rows }: { cols: number; rows: number }) => {
			if (ws?.readyState === WebSocket.OPEN) {
				ws.send(`\x1b[8;${rows};${cols}t`);
			}
		});

		// Window resize
		const resizeHandler = () => {
			if (fitAddon) fitAddon.fit();
		};
		window.addEventListener('resize', resizeHandler);

		return () => {
			window.removeEventListener('resize', resizeHandler);
		};
	}

	function connect() {
		const token = localStorage.token;
		const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
		const wsBase = WEBUI_API_BASE_URL.replace(/^https?:/, wsProtocol);
		const wsUrl = `${wsBase}/terminal/ws?token=${encodeURIComponent(token)}`;

		ws = new WebSocket(wsUrl);

		ws.onopen = () => {
			connected = true;
			terminal?.writeln('\r\n\x1b[32mConnected to terminal.\x1b[0m\r\n');
			if (fitAddon) {
				fitAddon.fit();
				const dims = fitAddon.proposeDimensions();
				if (dims && ws?.readyState === WebSocket.OPEN) {
					ws.send(`\x1b[8;${dims.rows};${dims.cols}t`);
				}
			}
		};

		ws.onmessage = (event) => {
			// Handle keepalive ping from backend
			if (event.data === '__ping__') {
				if (ws?.readyState === WebSocket.OPEN) {
					ws.send('__pong__');
				}
				return;
			}
			terminal?.write(event.data);
			// J-1-11: If output looks like a prompt return, notify file browser
			if (typeof event.data === 'string' && PROMPT_PATTERN.test(event.data)) {
				notifyFsChanged();
			}
		};

		ws.onclose = (event) => {
			connected = false;
			terminal?.writeln(`\r\n\x1b[31mDisconnected (code: ${event.code}).\x1b[0m`);
		};

		ws.onerror = () => {
			connected = false;
			terminal?.writeln('\r\n\x1b[31mConnection error.\x1b[0m');
		};
	}

	function disconnect() {
		ws?.close();
		ws = null;
		connected = false;
	}

	function reconnect() {
		disconnect();
		terminal?.clear();
		connect();
	}

	let cleanupResize: (() => void) | null = null;

	// J-1-11: Debounced filesystem change notification
	// When terminal output contains shell prompt indicators, signal file browser to refresh.
	let fsChangeTimer: ReturnType<typeof setTimeout> | null = null;
	const FS_CHANGE_DEBOUNCE_MS = 2000;

	function notifyFsChanged() {
		if (fsChangeTimer) clearTimeout(fsChangeTimer);
		fsChangeTimer = setTimeout(() => {
			window.dispatchEvent(new CustomEvent('terminal-fs-changed'));
			fsChangeTimer = null;
		}, FS_CHANGE_DEBOUNCE_MS);
	}

	// Detect shell prompt return (common patterns: $, #, >, %) after command output
	const PROMPT_PATTERN = /[\$#%>]\s*$/;

	onMount(async () => {
		cleanupResize = await initTerminal();
	});

	onDestroy(() => {
		cleanupResize?.();
		disconnect();
		terminal?.dispose();
		if (fsChangeTimer) clearTimeout(fsChangeTimer);
	});
</script>

<svelte:head>
	<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@xterm/xterm@5/css/xterm.min.css" />
</svelte:head>

<div class="flex flex-col h-full min-h-0">
	<div class="flex items-center justify-between py-2 flex-shrink-0">
		<div class="flex items-center gap-2">
			<div class="w-2 h-2 rounded-full {connected ? 'bg-green-500' : 'bg-red-500'}" />
			<span class="text-sm text-gray-500 dark:text-gray-400">
				{connected ? $i18n.t('Connected') : $i18n.t('Disconnected')}
			</span>
		</div>
		<button
			class="px-3 py-1 text-xs rounded-lg bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700 transition"
			on:click={reconnect}
		>
			{$i18n.t('Reconnect')}
		</button>
	</div>
	<div
		bind:this={terminalContainer}
		class="flex-1 rounded-lg overflow-hidden border border-gray-200 dark:border-gray-700"
		style="background: #1a1b26;"
	/>
</div>
