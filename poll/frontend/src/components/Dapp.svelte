<script>
    import { onMount } from "svelte";
    import { selectedAccount,web3 } from 'svelte-web3';
    import { abi,address } from "../contract";
    import Tabs from "./Tabs.svelte";
    import CreatePollForm from "./CreatePollForm.svelte";
    import PollList from "./PollList.svelte";

	let tabs = ['Current Polls','Add New Poll'];
	let activeTab = tabs[0];
    let voting;
    let isAdmin=false;
    let isLoaded=false;

    onMount(()=>{
        voting = new $web3.eth.Contract(abi,address);
        onAccountChange();
        isLoaded=true;
    })

    $: onAccountChange($selectedAccount);
    const onAccountChange = async()=>{
        if (voting){
            isAdmin = await voting.methods.isOwner().call({from:$selectedAccount});
            activeTab = tabs[0];
        }
    }

    const tabChange = (e) => {
		activeTab = e.detail
	}

</script>


<main class="my-8">

    {#if isLoaded}

        {#if isAdmin}
            <Tabs {tabs} {activeTab} on:tabChange={tabChange} />
        {/if}

        {#if activeTab==tabs[0]}
            <PollList {voting} />
        {:else if activeTab==tabs[1]}
            <CreatePollForm {voting} />
        {/if}

    {/if}

</main>

<style></style>