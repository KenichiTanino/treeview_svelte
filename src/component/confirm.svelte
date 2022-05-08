<script lang="ts">
  import { onMount } from "svelte";
  export let params;
  import "carbon-components-svelte/css/g100.css";
  import { ButtonSet, Button } from "carbon-components-svelte";
  import { content } from "../stores.js";
  import { querystring, push } from "svelte-spa-router";

  // API呼び出し
  const putContent = async (content) => {
    const serverURL = "http://localhost:8000/ft/" + params.fileid;
    const headers = {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    };
    const response = await fetch(serverURL, {
      method: "PUT",
      mode: "cors",
      credentials: "omit",
      headers: headers,
      body: JSON.stringify({ "content": content }),
    });
    const json = await response.json();
    // TODO: エラー処理
    return json;
  };
  import {parse} from 'qs';
  let filename = "";
  $: parsed = parse($querystring)

  onMount(()=>
    {
      filename = parsed.filename;
    }
  );

  function save() {
    putContent($content);
    push("/save/" + params.fileid );
  }

  function cancel() {
    push("/edit/" + params.fileid + "?filename=" + filename);
  }
</script>

<h2>content - {filename}</h2>
<div>
<pre>
{$content}
</pre>
</div>

<ButtonSet>
  <Button on:click={save}>保存</Button>
  <Button on:click={cancel}>前に戻る</Button>
</ButtonSet>

<style>
pre {border: 1px solid gray}
</style>