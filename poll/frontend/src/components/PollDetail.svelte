<script>
    import { onMount } from "svelte";
    import { selectedAccount,web3 } from 'svelte-web3';
    import { pollAbi } from "../contract";
    import Loading from "./Loading.svelte";

    export let pollAddress;
    let poll;
    let pollData = {
        question:"",
        options:[],
        totalVotes:0,
        voted:false
    };
    let loading=false;

    $: onAccountChange($selectedAccount);
    const onAccountChange = async()=>{
        if (poll) {
            getPollData();
        }
    }

    onMount(()=>{
        poll = new $web3.eth.Contract(pollAbi,pollAddress);
        getPollData();
    })

    const getPollData = async() => {
        pollData.voted = await poll.methods.voted($selectedAccount).call({from:$selectedAccount})
        pollData.question = await poll.methods.name().call({from:$selectedAccount})
        pollData.options = await poll.methods.getOptions().call({from:$selectedAccount})
        pollData.totalVotes = await poll.methods.totalVotes().call({from:$selectedAccount})
    }

    const handleVote = async(_id) => {
        loading=true;
        try {
            await poll.methods.vote(_id).send({from:$selectedAccount});
        } catch (error) {
            console.log(error);
        } finally {
            getPollData();
            loading=false;
        }
    }

    const calculatePercentage = (_votes)=>{
        return Math.floor(100*(_votes/pollData.totalVotes))
    }

</script>

<div class="border-2 rounded-xl shadow px-4 py-2 ">

    <h3 class="font-bold text-center">{pollData.question} ({pollData.voted ? "voted" : "not voted"})</h3>
    <span class="font-light text-red-500 ml-4 text‑transparent">total votes : {pollData.totalVotes}</span>
    
    {#if !loading}
        {#each pollData.options as option,idx}
        <div class="bg-gray-200 mx-4 mb-4 rounded text-lg">
            <div class="bg-blue-400 flex justify-between p-4" style="width: {calculatePercentage(option.count)}%">
                {#if !pollData.voted}
                    <button on:click="{()=>handleVote(idx)}" class="border-b-2 hover:text-yellow-400">{option.name}</button>
                {:else}
                    <div>{option.name}</div>
                {/if}
                <div class="ml-4">{option.count}</div>
            </div>
        </div>
        {/each}
    {:else}
        <Loading />
    {/if}
        

</div>