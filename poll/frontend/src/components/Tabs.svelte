<script>
    import { createEventDispatcher } from "svelte";
    const dispatch = createEventDispatcher();
    export let tabs;
    export let activeTab;
</script>

<div class="m-4 mb-4">
    <ul class="flex justify-evenly">
        {#each tabs as tab}
        <li class:border-b-4={tab===activeTab}  class:border-red-300={tab===activeTab}
        on:click="{()=>dispatch('tabChange',tab)}" >
            <div class:text-red-300={tab===activeTab} >{tab}</div>
        </li>
        {/each}
    </ul>
</div>

<style>
    li:hover {
    cursor: pointer;
}  
</style>