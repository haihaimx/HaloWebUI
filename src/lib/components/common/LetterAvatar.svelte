<script lang="ts">
	/**
	 * 首字母头像组件
	 * 取名称首字符 + 哈希选色，生成圆形彩色头像
	 */
	import { AVATAR_PALETTE, avatarHashCode } from '$lib/utils';

	export let name: string = '';
	export let size: string = 'size-7';
	export let className: string = '';
	export let textClass: string = '';

	function getInitial(s: string): string {
		const trimmed = (s ?? '').trim();
		if (!trimmed) return '?';
		const first = [...trimmed][0];
		if (/[a-zA-Z]/.test(first)) return first.toUpperCase();
		return first;
	}

	$: initial = getInitial(name);
	$: bgColor = AVATAR_PALETTE[avatarHashCode(name || '') % AVATAR_PALETTE.length];
</script>

<span
	class="letter-avatar inline-flex items-center justify-center rounded-xl shrink-0 select-none {size} {className}"
	style="background-color: {bgColor};"
	title={name}
>
	<span class="text-white font-bold leading-none {textClass}" style="font-size: 0.9em;">
		{initial}
	</span>
</span>

<style>
	.letter-avatar {
		box-shadow:
			0 1px 3px rgba(0, 0, 0, 0.1),
			0 1px 2px rgba(0, 0, 0, 0.06);
	}
</style>
