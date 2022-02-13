<script>
    import { onMount } from "svelte";
    import { web3 } from 'svelte-web3';
    import { abi,address } from "../contract";
    import Tabs from "./Tabs.svelte";
    import CreatePollForm from "./CreatePollForm.svelte";
    import PostList from "./PostList.svelte";

    let tabs = ['Post Feed','Create New Post'];
	let activeTab = tabs[0];
    let contract;
    let isLoaded = false;

    onMount(()=>{
        contract = new $web3.eth.Contract(abi,address);
        isLoaded = true;
    })

    const tabChange = (e) => {
		activeTab = e.detail
	}
    
</script>


<div>

    {#if isLoaded}
        <Tabs {tabs} {activeTab} on:tabChange={tabChange} />

        {#if activeTab==tabs[0]}
            <PostList {contract} />
        {:else if activeTab==tabs[1]}
            <CreatePollForm {contract} />
        {/if}
    {/if}

</div>

<style></style>