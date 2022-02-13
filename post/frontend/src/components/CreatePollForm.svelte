<script>
    import Loading from "./Loading.svelte";
    import { selectedAccount } from 'svelte-web3';

    export let contract;
    let title="";
    let content="";
    let loading=false;

    const submitHandler = async() => {
        loading=true;
        try {
            await contract.methods.createPost(title,content.value.trim()).send({from:$selectedAccount})
        } catch (error) {
            console.log(error);
        } finally {
            title="";
            content="";
            loading = false;
        }
    }
</script>

{#if !loading}
    <form class="w-1/3 mt-3 mx-auto" on:submit|preventDefault="{submitHandler}">
        <label for="title" class="font-semibold">Title :</label>
        <input type="text" id="title" bind:value="{title}"
        class="w-full bg-white rounded border border-gray-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 text-base outline-none text-gray-700 py-3 my-2 px-3 leading-8 transition-colors duration-200 ease-in-out">

        <label for="content" class="font-semibold">Content :</label>
        <textarea type="text" id="content" rows=3 bind:this="{content}"
        class="w-full bg-white rounded border border-gray-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 text-base outline-none text-gray-700 py-3 my-2 px-3 leading-8 transition-colors duration-200 ease-in-out">
        </textarea>
        <button class="text-white bg-indigo-500 border-0 py-2 px-6 focus:outline-none hover:bg-indigo-600 rounded text-lg">Create</button>
    </form>
{:else}
    <Loading />
{/if}