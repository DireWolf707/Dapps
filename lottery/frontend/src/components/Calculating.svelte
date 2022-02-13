<script>
    import Loading from "./Loading.svelte";
    export let contract;
    let fetch_players = contract.methods.getPlayers().call();
</script>


<div class="text-xl font-extrabold text-center my-2">
    Hold on! Winner is being calculated...
    <br>
    (Comeback later to know the Result)
</div>

<div class="border-t-2 my-2">
    {#await fetch_players}
        <Loading value={"Fetching data... "}/>
    {:then players} 
        <div class="font-semibold mt-2 text-center">Participants ({players.length})</div>
        {#each players as player}
            <div>
                {player}
            </div>
        {/each}
    {/await}
</div>