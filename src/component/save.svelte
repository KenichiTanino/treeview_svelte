<script lang="ts">
  import { onMount } from "svelte";
  export let params;

  import "carbon-components-svelte/css/g100.css";
  import { ButtonSet, Button } from "carbon-components-svelte";

  import { push } from "svelte-spa-router";

  function home() {
    push("/");
  }

  let fcontent;

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
  let filename;

  onMount(async () => {
    var file_content = await getContent();
    fcontent = file_content.content;
    filename = decodeURI(file_content.name);
  });
</script>

<h1>{filename}</h1>
<div>{fcontent}</div>

<ButtonSet>
  <Button on:click={home}>戻る</Button>
</ButtonSet>
