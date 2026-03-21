/**
 * marked.js inline extension for citation tokens.
 * Tokenizes [1], [1,2], [1#foo,2#bar] as first-class citation tokens.
 */

export function decodeString(str: string): string {
	try {
		return decodeURIComponent(str);
	} catch {
		return str;
	}
}

export function getDisplayTitle(title: string, maxLen = 30, startLen = 15, endLen = 10): string {
	const decoded = decodeString(title);
	if (decoded.startsWith('http://') || decoded.startsWith('https://')) {
		try {
			return new URL(decoded).hostname.replace(/^www\./, '');
		} catch {
			/* fall through */
		}
	}
	if (decoded.length <= maxLen) return decoded;
	return decoded.slice(0, startLen) + '\u2026' + decoded.slice(-endLen);
}

export function getTextFragmentUrl(doc: any): string | null {
	const { metadata, source, document: content } = doc ?? {};
	const { file_id, page } = metadata ?? {};
	const sourceUrl = source?.url;

	const baseUrl = file_id
		? `/api/v1/files/${file_id}/content${page !== undefined ? `#page=${page + 1}` : ''}`
		: sourceUrl?.includes('http')
			? sourceUrl
			: null;

	if (!baseUrl || !content) return baseUrl;

	const words = content
		.trim()
		.replace(/\s+/g, ' ')
		.split(' ')
		.filter((w: string) => w.length > 0 && !/https?:\/\/|[\u{1F300}-\u{1F9FF}]/u.test(w));

	if (words.length === 0) return baseUrl;

	const clean = (w: string) => w.replace(/[^\w]/g, '');
	const first = clean(words[0]);
	const last = clean(words.at(-1));
	const fragment = words.length === 1 ? first : `${first},${last}`;

	return fragment ? `${baseUrl}#:~:text=${fragment}` : baseUrl;
}

function citationExtension(sourceIdsRef: { current: string[] }) {
	return {
		name: 'citation',
		level: 'inline' as const,

		start(src: string) {
			const match = src.match(/\[\d/);
			return match ? match.index : -1;
		},

		tokenizer(src: string) {
			// Avoid matching footnotes
			if (/^\[\^/.test(src)) return;

			// Match [1], [1,2], [1#foo], [1#foo,2#bar], and adjacent groups like [1][2,3]
			const rule = /^(\[(?:\d+(?:#[^,\]\s]+)?(?:,\s*\d+(?:#[^,\]\s]+)?)*)\])+/;
			const match = rule.exec(src);
			if (!match) return;

			const raw = match[0];
			const ids = sourceIdsRef.current;

			// Extract all bracket groups
			const groupRegex = /\[([^\]]+)\]/g;
			const citations: { index: number; title: string; identifier: string }[] = [];
			let m: RegExpExecArray | null;

			while ((m = groupRegex.exec(raw))) {
				const parts = m[1].split(',').map((p) => p.trim());
				for (const part of parts) {
					const partMatch = /^(\d+)(?:#(.+))?$/.exec(part);
					if (partMatch) {
						const index = parseInt(partMatch[1], 10);
						if (index >= 1 && index <= ids.length) {
							citations.push({
								index,
								title: ids[index - 1] ?? 'N/A',
								identifier: part
							});
						}
					}
				}
			}

			if (citations.length === 0) return;

			return {
				type: 'citation',
				raw,
				citations
			};
		},

		renderer(token: any) {
			return token.raw;
		}
	};
}

export default function (sourceIdsRef: { current: string[] }) {
	return {
		extensions: [citationExtension(sourceIdsRef)]
	};
}
