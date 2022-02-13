<script>
    import Public from "./Public.svelte";
    import Owner from "./Owner.svelte";
    import Loading from "./Loading.svelte";
    import { onMount } from "svelte";
    import { selectedAccount,web3 } from 'svelte-web3';
    import { abi,address } from "../contract";

    let contract;
    let loaded=false;
    let isOwner=false;
    let data;

    onMount(async ()=>{
        contract = new $web3.eth.Contract(abi,address);
        getData();
        isOwner = await contract.methods.isOwner().call({from:$selectedAccount});
        loaded=true;
    })

    $: onAccounChange($selectedAccount)
    const onAccounChange = async()=>{
        if (contract) {
            isOwner = await contract.methods.isOwner().call({from:$selectedAccount})
        }
    }

    const getData = async ()=>{
        let _count = await contract.methods.count().call({from:$selectedAccount});
        let _topFunder = await contract.methods.topFunder().call({from:$selectedAccount});
        let _topFunderAmount = await contract.methods.addressToAmountFunded(_topFunder).call({from:$selectedAccount});
        let _recentFunders = []

        let _address;
        for (let i = 0; i < Math.min(5,_count); i++) {
            _address = await contract.methods.funders(_count - (i+1)).call({from:$selectedAccount});
            _recentFunders.push(_address)
        }

        data = {
            topFunder:_topFunder,
            topFunderAmount:$web3.utils.fromWei(_topFunderAmount,"ether"),
            recentFunders:_recentFunders,
        };
    }
</script>


{#if loaded}
<div class="my-2 mx-3 p-1 border-2 rounded-lg bg-gray-100">
    <div class="flex justify-between content-center text-lg">
        <div class="text-2xl my-auto font-bold">FundMe</div>
        <div>
            {#if isOwner}
                <Owner {contract} />
            {:else}
                <Public {contract} on:getData={getData}/>
            {/if}
        </div>
    </div>
</div>

<div class="flex mx-2 p-2">
    <div class="w-3/5"></div>

    <div class="w-2/5 text-center border-2 rounded p-2">
        {#if data}

            <div class="border-b-2 p-2 rounded-lg font-bold">
                <div class="text-xl">
                    Top Donation 
                </div>
                {data.topFunder} ({data.topFunderAmount} ETH)
            </div>
            
            <div class="text-md font-bold">
                Recent 5 Donation 
            </div>
            {#each data.recentFunders as funder}
                <div>
                    {funder}
                </div>
            {/each}
    
        {:else}
            <Loading value={"Loading... "} />
        {/if}
    </div>

</div>

{/if}

<style></style>