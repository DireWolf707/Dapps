<script>
    import { selectedAccount,web3 } from 'svelte-web3';
    import { createEventDispatcher } from "svelte";
    import Loading from "./Loading.svelte";

    export let contract;
    let loading=false;
    let dispatch=createEventDispatcher();
    let funding=false;
    let usd=1;
    let ether;

    $: onAmountChange(usd,funding)
    const onAmountChange = async ()=>{
        if(funding){
            ether = "calculating... " ;
            if(usd>=1){
                let _ether = await contract.methods.getConversionRate(usd).call({from:$selectedAccount});
                ether = _ether / 10**8;
            }
            else{
                ether=">=0"
            }
        }
    }

    const fund = async ()=>{
        loading=true;
        try {
            await contract.methods.fund().send({
                from:$selectedAccount,
                value:$web3.utils.toWei(
                    String(ether),
                    "ether"
                )
            });
            dispatch('getData');
        } catch (error) {
            console.log(error);
        } finally {
            funding=false;
            usd=1;
            loading=false;
        }
    }
</script>

{#if !loading}

    {#if !funding}
    <button on:click="{()=>funding=!funding}"
        class="border px-2 py-1 rounded bg-yellow-300">
        Donate
    </button>
    {:else}
    <input type="number" min=1 bind:value="{usd}" class="w-9 rounded-lg">$ ({ether} ETH) &nbsp;
    <button on:click="{fund}"
        class="border px-2 py-1 rounded bg-yellow-300">
        Send
    </button>
    {/if}

{:else}
    <Loading padding={2} />
{/if}