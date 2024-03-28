<script lang="ts">
	import { copyToClipboard } from '$lib/utils';
	import { runCode } from '$lib/apis/code';
	import hljs from 'highlight.js';
	import 'highlight.js/styles/github-dark.min.css';

	export let lang = '';
	export let code = '';

	let copied = false;

	const copyCode = async () => {
		copied = true;
		await copyToClipboard(code);

		setTimeout(() => {
			copied = false;
		}, 1000);
	};

	let running = false;
	let runResponse: {output: string, error: string} | null = null;

	const runCodeClicked = async () => {
		running = true;
		runResponse = await runCode(localStorage.token, code, "python");
		running = false;
	}

	$: highlightedCode = code ? hljs.highlightAuto(code, hljs.getLanguage(lang)?.aliases).value : '';
</script>

{#if code}
	<div class="mb-4">
		<div
			class="flex justify-end bg-[#202123] text-white text-xs px-4 pt-1 pb-0.5 rounded-t-lg overflow-x-auto"
		>
			<div class="p-1">{@html lang}</div>
			<button class="bg-none border-none p-1" on:click={runCodeClicked}
				>{running? 'Running' : 'Run Code'}</button>
			<button class="copy-code-button bg-none border-none p-1" on:click={copyCode}
				>{copied ? 'Copied' : 'Copy Code'}</button
			>
		</div>

		<pre class=" rounded-b-lg hljs p-4 px-5 overflow-x-auto rounded-t-none"><code
				class="language-{lang} rounded-t-none whitespace-pre">{@html highlightedCode || code}</code
			></pre>
	</div>
{/if}
{#if runResponse}
	<div class="mt-4">
		{#if runResponse.output}
			<pre class="rounded-lg hljs p-4 px-5 overflow-x-auto rounded-t-none"><code
					class="language-{lang} rounded-t-none whitespace-pre">{@html runResponse.output}</code
				></pre>
		{/if}
		{#if runResponse.error}
			<pre class="rounded-lg hljs p-4 px-5 overflow-x-auto rounded-t-none bg-red-200 text-red-800"><code
					class="language-{lang} rounded-t-none whitespace-pre">Error: {@html runResponse.error}</code
				></pre>
		{/if}
	</div>
{/if}
