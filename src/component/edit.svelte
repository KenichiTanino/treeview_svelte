<script lang="ts">
  import { onMount } from "svelte";

  export let params;
  import "carbon-components-svelte/css/g100.css";
  import { TextArea, ButtonSet, Button } from "carbon-components-svelte";
  import { content } from "../stores.js";
  import { push } from "svelte-spa-router";

  let filename = "";

  function confirm() {
    push("/confirm/" + params.fileid + "?filename=" + filename);
  }

  function cancel() {
    push("/");
  }

  // API呼び出し
  const getContent = async () => {
    const serverURL = "http://localhost:8000/ft/" + params.fileid;
    const response = await fetch(serverURL, {
      method: "GET",
      mode: "cors",
      credentials: "omit",
    });
    const json = await response.json();
    return json;
  };

  onMount(async () => {
    var file_content = await getContent();
    $content = file_content.content;
    filename = decodeURI(file_content.name);
  });
</script>

<main>
  <TextArea
    labelText="Content - {filename}"
    bind:value={$content}
    placeholder="content..."
    rows={20}
  />

  <ButtonSet>
    <Button on:click={confirm}>確認</Button>
    <Button on:click={cancel}>キャンセル</Button>
  </ButtonSet>
</main>

<style>
</style>
