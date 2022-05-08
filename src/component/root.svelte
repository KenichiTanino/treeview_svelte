<script lang="ts">
  import "carbon-components-svelte/css/g100.css";
  import Folder from "carbon-icons-svelte/lib/Folder16";
  import File from "carbon-icons-svelte/lib/DocumentBlank16";

  import { Header, HeaderNav, Content } from "carbon-components-svelte";

  import {
    TreeView,
    ButtonSet,
    Button,
    Modal,
    TextInput,
    Form,
  } from "carbon-components-svelte";
  import { onMount } from "svelte";
  import { push } from "svelte-spa-router";

  // API呼び出し
  const getFolders = async () => {
    const serverURL = "http://localhost:8000/ft/";
    const response = await fetch(serverURL, {
      method: "GET",
      mode: "cors",
      credentials: "omit",
    });
    const json = await response.json();
    return json;
  };

  // tree view画面系統
  let treeview = null;
  let expandedIds = [];
  let activeId = 0;
  let selectedIds = [];
  let children;
  let treetypes = {};

  //iconを指定する
  function change_node(node) {
    if (node["type"] == "DocumentBlank") {
      node["icon"] = File;
    } else if (node["type"] == "Folder") {
      node["icon"] = Folder;
    }
    // 型だけ削除前にとっておく
    treetypes[node["id"]] = node["type"];
    delete node["type"];
    expandedIds.push(node["id"]);
    for (let index in node["children"]) {
      change_node(node["children"][index]);
    }
  }

  // アプリマウント時に、treeを指定する
  onMount(async () => {
    var folders = await getFolders();
    for (let index in folders) {
      change_node(folders[index]);
    }
    children = folders;
    treeview.expandAll;
  });

  // id to type (NOT YET IMPREMENT)
  function id_to_type(id) {
    console.log(treetypes[id]);
  }

  // ダイアログ関連
  let openDelete = false;
  let openCreateFilename = false;
  let form;

  let inputFilenameValue;

  function create_file_new() {
    console.log("creawte file new");
    // TODO: NEED IMPREMENT
    openCreateFilename = true;
  }

  function create_file_new_submit() {
    id_to_type(activeId);
    openCreateFilename = false;
  }

  function edit() {
    push("/edit/" + activeId);
  }

  function remove() {
    // TODO: NEED IMPREMENT
    openDelete = true;
  }

  function remove_confirm() {
    // TODO: NEED IMPREMENT
    openDelete = false;
  }
</script>

<Header platformName="TreeView_Svelte">
  <HeaderNav />
</Header>

<Content>
  <TreeView
    labelText="Tree View File Folder"
    {children}
    bind:activeId
    bind:selectedIds
    bind:expandedIds
    bind:this={treeview}
  />
  <ButtonSet>
    <!-- <Button on:click={create_folder_new} >フォルダ新規作成</Button> -->
    <Button on:click={create_file_new}>ファイル新規作成</Button>
    <Button on:click={edit}>編集</Button>
    <Button on:click={remove} kind="danger-tertiary">削除</Button>
  </ButtonSet>
  <!-- <div>Active node id: {activeId}</div>
  <div>Selected ids: {JSON.stringify(selectedIds)}</div> -->

  <Modal
    danger
    bind:open={openDelete}
    modalHeading="Delete File"
    primaryButtonText="削除"
    secondaryButtonText="Cancel"
    on:click:button--secondary={() => (openDelete = false)}
    on:click:button--primary={remove_confirm}
    on:open
    on:close
    on:submit
  >
    <p>フォルダ/ファイルを削除します。続けるなら削除を押下してください</p>
  </Modal>

  <Modal
    bind:open={openCreateFilename}
    shouldSubmitOnEnter={false}
    primaryButtonText="設定"
    secondaryButtonText="キャンセル"
    selectorPrimaryFocus=".bx--text-input"
    modalHeading="Filename 設定"
    hasForm
    on:click:button--secondary={() => (openCreateFilename = false)}
    on:submit={() => (form.reportValidity() ? create_file_new_submit() : null)}
  >
    <Form on:submit={create_file_new_submit} bind:ref={form}>
      <TextInput
        labelText="File name"
        placeholder="Enter File name..."
        bind:value={inputFilenameValue}
        required
      />
    </Form>
  </Modal>
</Content>

<style>
</style>
