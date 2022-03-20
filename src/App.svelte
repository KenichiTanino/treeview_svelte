<script lang="ts">
	import "carbon-components-svelte/css/g100.css";
	import Folder from "carbon-icons-svelte/lib/Folder16";
	import File from "carbon-icons-svelte/lib/DocumentBlank16";
	import {
    	Header,
    	HeaderNav,
    	Content,
		TreeView,
  	} from "carbon-components-svelte";
	let activeId = 1;
	let selectedIds = [];
    let children = [
    { id: 0, text: "AI / Machine learning", icon: Folder },
    {
      id: 1,
      text: "Analytics",
      icon: Folder,
      expanded: true,
      children: [
        {
          id: 2,
          text: "IBM Analytics Engine",
          icon: Folder,
          expanded: true,
          children: [
            { id: 3, text: "Apache Spark", icon: File },
            { id: 4, text: "Hadoop", icon: File },
          ],
        },
        { id: 5, text: "IBM Cloud SQL Query", icon: File },
        { id: 6, text: "IBM Db2 Warehouse on Cloud", icon: File },
      ],
    },
    {
      id: 7,
      text: "Blockchain",
      icon: Folder,
      children: [
        { id: 8, text: "IBM Blockchain Platform", icon: File },
      ],
    },
    {
      id: 9,
      text: "Databases",
      icon: Folder,
      children: [
        {
          id: 10,
          text: "IBM Cloud Databases for Elasticsearch",
          icon: File,
        },
        {
          id: 11,
          text: "IBM Cloud Databases for Enterprise DB",
          icon: File,
        },
        { id: 12, text: "IBM Cloud Databases for MongoDB", icon: File },
        {
          id: 13,
          text: "IBM Cloud Databases for PostgreSQL",
          icon: File,
        },
      ],
    },
    {
      id: 14,
      text: "Integration",
      icon: Folder,
      disabled: true,
      children: [
        {
          id: 15,
          text: "IBM API Connect",
          icon: File,
          disabled: true,
        },
      ],
    },
  ];	
</script>

<main>
	<Header platformName="TreeView_Svelte">
		<HeaderNav>
		</HeaderNav>
	</Header>
	  
	<Content>
		<TreeView
		labelText="File Folder Sample"
		{children}
		bind:activeId
		bind:selectedIds
		on:select={({ detail }) => console.log("select", detail)}
		on:toggle={({ detail }) => console.log("toggle", detail)}
		on:focus={({ detail }) => console.log("focus", detail)}
	  />
	  <div>Active node id: {activeId}</div>
      <div>Selected ids: {JSON.stringify(selectedIds)}</div>
    </Content>
</main>

<style>

</style>