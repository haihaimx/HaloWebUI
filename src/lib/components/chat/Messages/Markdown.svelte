<script>
	import { marked } from 'marked';
	import { replaceTokens, processResponseContent } from '$lib/utils';
	import { user } from '$lib/stores';
	import { getModelChatDisplayName } from '$lib/utils/model-display';

	import markedExtension from '$lib/utils/marked/extension';
	import markedKatexExtension from '$lib/utils/marked/katex-extension';
	import citationExtension from '$lib/utils/marked/citation-extension';

	import MarkdownTokens from './Markdown/MarkdownTokens.svelte';
	import { createEventDispatcher } from 'svelte';

	const dispatch = createEventDispatcher();

	export let id = '';
	export let content;
	export let model = null;
	export let save = false;

	export let sourceIds = [];

	export let onSourceClick = () => {};
	export let onTaskClick = () => {};

	let tokens = [];

	// Mutable ref for sourceIds — the citation extension reads this at tokenize time
	let sourceIdsRef = { current: [] };
	$: sourceIdsRef.current = sourceIds;

	// 创建禁用单波浪号删除线的扩展
	// marked.js v9 默认支持 ~text~ 和 ~~text~~ 都解析为删除线
	// 这不符合 GFM 规范，只应该支持 ~~text~~
	function noSingleTildeExtension() {
		return {
			name: 'noSingleTilde',
			level: 'inline',
			walkTokens(token) {
				// 将单波浪号的 del token 转换为 text token
				if (token.type === 'del') {
					const raw = token.raw || '';
					// 如果是单波浪号格式，转换为文本
					if (/^~[^~]+~$/.test(raw) && !/^~~[^~]+~~$/.test(raw)) {
						token.type = 'text';
					}
				}
			}
		};
	}

	const options = {
		throwOnError: false
	};

	marked.use(markedKatexExtension(options));
	marked.use(markedExtension(options));
	marked.use(citationExtension(sourceIdsRef));
	marked.use(noSingleTildeExtension());

	// 修复 CJK 字符导致 marked.js emphasis（加粗/斜体）解析失败的问题。
	// 根因：CommonMark emphasis 的 left/right-flanking 规则用 \p{P} 判断标点边界，
	// CJK 字符属于 \p{L}（字母），不被视为标点——当 CJK 紧邻 ** 且另一侧是 Unicode 标点时，
	// flanking 判定失败，** 被当作普通文本。
	// 修复：在 tokenizer 的 punctuation / rDelimAst / rDelimUnd 正则中注入 CJK 范围，
	// 使 CJK 字符被视为"标点"（仅影响 emphasis 边界判定）。
	// 注意：不修改 lDelim，否则 CJK 字符会被捕获到 Group 1（标点组）导致回归。
	{
		const CJK = '\u4e00-\u9fff\u3400-\u4dbf\u3040-\u309f\u30a0-\u30ff\uac00-\ud7af\uf900-\ufaff';
		const addCJK = (re) => new RegExp(re.source.replaceAll('\\p{P}', '\\p{P}' + CJK), re.flags);
		marked.use({
			tokenizer: {
				emStrong(src, maskedSrc, prevChar) {
					if (!this.rules.inline._cjkPatched) {
						this.rules.inline.punctuation = addCJK(this.rules.inline.punctuation);
						this.rules.inline.emStrong.rDelimAst = addCJK(this.rules.inline.emStrong.rDelimAst);
						this.rules.inline.emStrong.rDelimUnd = addCJK(this.rules.inline.emStrong.rDelimUnd);
						this.rules.inline._cjkPatched = true;
					}
					return marked.Tokenizer.prototype.emStrong.call(this, src, maskedSrc, prevChar);
				}
			}
		});
	}

	// J-3-02: Cache the last processed string to skip re-lexing when content hasn't changed.
	// During streaming, Svelte reactive blocks fire on every history.messages assignment
	// even if this particular message's content is identical.
	let _lastProcessed = '';

	$: (async () => {
		if (content) {
			const processed = replaceTokens(
				processResponseContent(content),
				getModelChatDisplayName(model),
				$user?.name
			);
			if (processed !== _lastProcessed) {
				_lastProcessed = processed;
				tokens = marked.lexer(processed);
			}
		}
	})();
</script>

{#key id}
	<MarkdownTokens
		{tokens}
		{id}
		{save}
		{onTaskClick}
		{onSourceClick}
		on:update={(e) => {
			dispatch('update', e.detail);
		}}
		on:code={(e) => {
			dispatch('code', e.detail);
		}}
	/>
{/key}
