<script>
    import { onMount } from "svelte";
    import { selectedAccount,web3 } from 'svelte-web3';
    import Loading from "./Loading.svelte";

    export let contract;
    let amount;

    onMount(async ()=>{
        getCurrentFunds();
    })

    const getCurrentFunds = async ()=>{
        let _amount = await contract.methods.currentFunds().call({from:$selectedAccount});
        amount = $web3.utils.fromWei(_amount,"ether");
    }

    const withdraw = async ()=>{
        amount = undefined;
        try {
            await contract.methods.withdraw().send({from:$selectedAccount});
        } catch (error) {
            console.log(error);
        } finally {
            getCurrentFunds();
        }
    }
</script>

{#if amount}
    {amount} ETH 
    &nbsp;
    <button on:click="{withdraw}"
        class="border px-2 py-1 rounded bg-yellow-300">
        Withdraw
    </button>
{:else}
    <Loading padding={2} value={"Loading... "} />
{/if}

