<script lang="ts">

  // 画面遷移
  import Router from 'svelte-spa-router'
  import Edit from "./component/edit.svelte";
  import Confirm from "./component/confirm.svelte";
  import Save from "./component/save.svelte";
  import Root from "./component/root.svelte";

  const routes = {
        '/edit/:fileid': Edit,
		'/confirm/:fileid': Confirm,
		'/save/:fileid': Save,
		'/': Root,
  };

</script>

<main>
	<Router routes={routes}></Router>
</main>

<style>

</style>