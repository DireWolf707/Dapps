<script>
    import { onMount } from "svelte";
    import { selectedAccount,web3 } from 'svelte-web3';
    import { abi,address } from "../contract";
    import Loading from "./Loading.svelte";
    import Open from "./Open.svelte";
    import Calculating from "./Calculating.svelte";
    import Closed from "./Closed.svelte";

    let contract;
    let loading=false;
    let lotteryState;
    let isOwner=false;

    onMount(()=>{
        contract = new $web3.eth.Contract(abi,address);
        onAccountChanage();
    })

    $:onAccountChanage($selectedAccount)
    const onAccountChanage = async ()=>{
        if (contract) {
            isOwner = await contract.methods.isOwner().call({from:$selectedAccount});
            getLotteryStatus()
        }
    }

    const getLotteryStatus = async ()=>{
        lotteryState = await contract.methods.lottery_state().call({from:$selectedAccount});
    }

    const toggleLoading = ()=>{
        loading = !loading;
    }
</script>


<div class="w-1/3 mx-auto border-2 rounded-lg mt-24">
    
        <div class="border-b-4 text-3xl font-extrabold text-center p-2 bg-gray-200">
            Lottery
        </div>
        <div class="grid grid-cols-1 justify-items-center p-2">
            {#if lotteryState && !loading}
                {#if lotteryState==0}
                    <Open {contract} {isOwner} on:toggleLoading={toggleLoading} on:getLotteryStatus={getLotteryStatus}/>
                {:else if lotteryState==1}
                    <Closed {contract} {isOwner} on:toggleLoading={toggleLoading} on:getLotteryStatus={getLotteryStatus}/>
                {:else}
                    <Calculating {contract}/>
                {/if}
            {:else if !lotteryState && !loading}
                <Loading value={"Fetching Data... "}/>
            {:else if lotteryState && loading}
                <Loading />
            {/if}
        </div>
</div>

<style></style>