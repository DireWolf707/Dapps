<script>
    import PollDetail from "./PollDetail.svelte";
    import { onMount } from "svelte";
    import { selectedAccount } from 'svelte-web3';

    export let voting;
    let polls=[];

    onMount(()=>{
        getPolls();
    })

    const getPolls = async() => {
        let _polls = await voting.methods.getPolls().call({from:$selectedAccount});
        _polls = [..._polls].reverse();
        polls = _polls;
    }

</script>

<div class="grid grid-cols-1 gap-4 w-1/3 mx-auto">
    {#each polls as pollAddress}
        <PollDetail {pollAddress} />
    {/each}
</div>