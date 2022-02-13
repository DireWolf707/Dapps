<script>
    import { onMount } from "svelte";
    import { createEventDispatcher } from "svelte";
    import { selectedAccount,web3 } from 'svelte-web3';
    import Loading from "./Loading.svelte";

    export let isOwner;
    export let contract;
    let players;
    let count;
    let userEntered;
    let entranceFee="fetching... ";
    let amountPoolEth="fetching... ";
    let amountPoolUsd="fetching... ";
    let dispatch = createEventDispatcher();

    onMount(()=>{
        getLotteryData()
    })

    $:onAccountChange($selectedAccount)
    const onAccountChange = ()=>{
        userEntered=undefined;
        if (contract) {
            getLotteryData();
        }
    }

    const getLotteryData = async ()=>{
        players = await contract.methods.getPlayers().call({from:$selectedAccount});
        count = players.length;

        let _amountPoolEth = await $web3.eth.getBalance(contract.options.address);
        amountPoolEth = _amountPoolEth / 10**18;
        let _ethPrice = await contract.methods.getPrice().call({from:$selectedAccount});
        amountPoolUsd = Math.round(amountPoolEth * (_ethPrice/10**8));

        let _entranceFee = await contract.methods.getEntranceFee().call({from:$selectedAccount});
        entranceFee = _entranceFee / 10**18;

        userEntered = await contract.methods.playerEntered($selectedAccount).call({from:$selectedAccount});
    }

    const endLottery = async ()=>{
        try {
            dispatch('toggleLoading');
            await contract.methods.endLottery().send({from:$selectedAccount});
            dispatch("getLotteryStatus");
        } catch (error) {
            console.log(error);
        } finally {
            dispatch('toggleLoading');
        }
    }

    const enterLottery = async ()=>{
        try {
            dispatch('toggleLoading');
            let _entranceFee = await contract.methods.getEntranceFee().call({from:$selectedAccount});
            await contract.methods.enter().send({from:$selectedAccount,value:_entranceFee});
        } catch (error) {
            console.log(error);
        } finally {
            getLotteryData();
            dispatch('toggleLoading');
        }
    }
</script>

{#if userEntered != undefined}
<div> 
    {#if isOwner}
    <button on:click="{endLottery}"
        class="border rounded-md bg-yellow-400 hover:bg-yellow-300 text-white px-3 py-2 my-2">Close</button>
    {:else}
        {#if userEntered}
            <div class="text-md underline underline-offset-4 my-2">
                You have entered the lottery!
            </div>
        {:else}
        <button on:click="{enterLottery}"
            class="border rounded-md bg-yellow-400 hover:bg-yellow-300 text-white px-3 py-2 my-2">Enter</button> 
        {/if}
    {/if}
</div>

<div class="font-semibold">
    Entery Amount : 50$ ({entranceFee} ETH)
</div>
<div class="font-semibold">
    Amount Pool : {amountPoolUsd}$ ({amountPoolEth} ETH)
</div>
<div class="border-t-2 my-2">
    <div class="font-semibold mt-2 text-center">Participants ({count})</div>
    {#each players as player}
    <div>
        {player}
    </div>
    {/each}
</div>
{:else}
    <Loading value={"Fetching Data... "}/>
{/if}