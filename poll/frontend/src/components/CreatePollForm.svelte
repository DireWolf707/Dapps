<script>
    import { selectedAccount } from 'svelte-web3';
    import Loading from "./Loading.svelte";

    export let voting;
    let loading=false;
    let numOfOptions=2;
    let formData = {
        question : '',
        options : [],
    }

    const submitHandler = async() => {
        loading=true;
        try {
            await voting.methods.createPoll(formData.question,formData.options).send({from:$selectedAccount});
        } catch (error) {
            console.log(error);
        } finally {
            formData = {
                question : '',
                options : [],
            }
            numOfOptions=2;
            loading=false;
        }
    }

</script>

{#if !loading}
    <form class="w-1/3 mt-3 mx-auto" on:submit|preventDefault="{submitHandler}">
        <div>
            <label for="question">Poll Ques :</label>
            <input type="text" id="question" bind:value="{formData.question}"
            class="w-full bg-white rounded border border-gray-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 text-base outline-none text-gray-700 py-3 my-2 px-3 leading-8 transition-colors duration-200 ease-in-out">
        
            <label for="options" class="font-semibold">#Options:</label>
            <input type="number" id="options" min="2" bind:value="{numOfOptions}" class="w-1/6 border-b-2 mb-2 font-semibold">
        </div>
        
        {#each Array(numOfOptions) as _, idx}
            <div>
                <label for="answer">Option {idx+1} :</label>
                <input type="text" id="answer" bind:value="{formData.options[idx]}"
                class="w-full bg-white rounded border border-gray-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 text-base outline-none text-gray-700 py-3 my-2 px-3 leading-8 transition-colors duration-200 ease-in-out">
            </div>
        {/each}

        <button class="text-white bg-indigo-500 border-0 py-2 px-6 focus:outline-none hover:bg-indigo-600 rounded text-lg">Create</button>
    </form>
{:else}
    <Loading />
{/if}

