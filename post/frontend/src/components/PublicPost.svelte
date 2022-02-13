<script>
    import { selectedAccount,web3 } from "svelte-web3";
    import { createEventDispatcher } from "svelte";

    export let id;
    export let contract;

    let dispatch=createEventDispatcher();
    let tiping=false;
    let usd=1;
    let ether;

    $:getConversionRate(usd,tiping);
    const getConversionRate = async() => {
        if (tiping) {
            ether = "calculating... " ;
            if(usd>=1){
                let _ether = await contract.methods.getConversionRate(usd).call({from:$selectedAccount});
                ether = _ether/10**8;
            }
            else{
                ether=">=0"
            }
        }
    }

    const tipPost = async() => {
        dispatch('changeLoading');
        try {
            await contract.methods.tipPost(id).send({
                from:$selectedAccount,
                value:$web3.utils.toWei(
                    String(ether),
                    "ether"
                )
            }); 
        } catch (error) {
            console.log(error);
        } finally {
            dispatch('getPost');
            usd=1;
            tiping=false;
        }
    }

</script>


{#if !tiping}
<button on:click="{()=>tiping=!tiping}"
    class="border-2 rounded bg-blue-200 hover:bg-yellow-300 px-3 py-1">tip</button>
{:else}
    <div>
        <input bind:value="{usd}"
        type="number" class="border-2 rounded w-9" min="1">$ ({ether}ETH)
        <button on:click="{tipPost}"
            class="border-2 rounded bg-yellow-300 hover:bg-red-400 px-3 py-1">confirm</button>
    </div>
{/if}
