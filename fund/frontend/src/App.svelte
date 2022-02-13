<script>
    import { onMount } from "svelte";
    import { defaultEvmStores,connected,selectedAccount,chainId } from 'svelte-web3';
    import Dapp from "./components/Dapp.svelte"

    let development = false;
    $: chain = development ? "Localhost" : "Rinkeby";

    async function connectWallet(){
        await defaultEvmStores.setProvider();
    }

    onMount(()=>{
        connectWallet()
    })
</script>

<main>
  {#if $connected && $selectedAccount}
        {#if development && ($chainId == 1337 || $chainId == "0x539")}
            <Dapp />
        {:else if !development && ($chainId == 4 || $chainId == "0x4")}
            <Dapp />
        {:else}
            <span class="text-5xl flex items-center justify-center h-screen">Change Network to {chain}!</span> 
        {/if}
    {:else}
        <span class="text-5xl flex items-center justify-center h-screen">Connect to MetaMask!</span>
    {/if}
</main>

<style>
  
</style>
