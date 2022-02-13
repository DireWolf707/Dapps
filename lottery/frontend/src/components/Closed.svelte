<script>
    import { onMount } from "svelte";
    import { createEventDispatcher } from "svelte";
    import { selectedAccount } from 'svelte-web3';
    import Loading from "./Loading.svelte";

    export let isOwner;
    export let contract;
    let lastWinner;
    let dispatch = createEventDispatcher();

    onMount(()=>{
        getLotteryData()
    })

    const getLotteryData = async ()=>{
        lastWinner = await contract.methods.lastWinner().call({from:$selectedAccount});
    }

    const startLottery = async()=>{
        try {
            dispatch("toggleLoading");
            await contract.methods.startLottery().send({from:$selectedAccount});
            dispatch("getLotteryStatus");
        } catch (error) {
            console.log(error);
        } finally {
            dispatch("toggleLoading");
        }
    }
</script>

<div class="text-xl font-bold">
    Closed!
</div>

{#if isOwner}
    <button on:click="{startLottery}"
    class="border rounded-md bg-yellow-400 hover:bg-yellow-300 text-white px-3 py-2 my-2">OPEN!</button>
{/if}

<div class="font-semibold mb-2">
    {#if lastWinner}
        <div class="underline underline-offset-1">
            Last Winner
        </div>
        {lastWinner}
    {:else}
        <Loading value={"Fetching Last Winner..."} padding={6}/>
    {/if}
</div>