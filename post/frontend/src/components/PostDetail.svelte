<script>
    import { selectedAccount,web3 } from "svelte-web3";
    import Loading from "./Loading.svelte";
    import PublicPost from "./PublicPost.svelte";

    export let id;
    export let contract;
    export let post;

    let loading=false;
    let updating=false;
    let content="";
    let title="";

    $: author = (post.author).toLowerCase();
    $: postTip = $web3.utils.fromWei(String(post.tip),"ether");
    
    const changeLoading = ()=>{
        loading=!loading;
    }

    const getPost = async ()=>{
        post = await contract.methods.posts(id).call({from:$selectedAccount});
        changeLoading();
    }

    const updatePost = async ()=>{
        changeLoading();
        try {
            await contract.methods.updatePost(title,content.trim(),id).send({from:$selectedAccount});
        } catch (error) {
            console.log(error);
        } finally {
            updating=false;
            content="";
            title="";
            getPost();
        }
    }

    const udpateHandler = ()=>{
        title = post.title;
        content = post.content;
        updating = true;
    }
    
</script>


<div class="border rounded p-4 my-4">
    {#if !loading}

        {#if !updating}

            <p class="font-bold text-xl border-b-2 break-words">
                {post.title}
            </p>
            <p class=" text-lg mt-2 break-words">
                {post.content}
            </p>
            <div class="flex justify-between border-t-2 mt-4 pt-2">
                {postTip}ETH tipped

                {#if author == $selectedAccount}
                    <button on:click="{udpateHandler}"
                        class="border-2 rounded bg-blue-200 hover:bg-yellow-300 px-3 py-1">update</button>
                {:else}
                    <PublicPost {id} {contract} on:changeLoading={changeLoading} on:getPost={getPost} />
                {/if}
            </div>

        {:else}

            <form on:submit|preventDefault="{updatePost}">
                <label for="title" class="font-semibold">Title :</label>
                <input type="text" id="title" bind:value="{title}"
                class="w-full bg-white rounded border border-gray-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 text-base outline-none text-gray-700 py-3 my-2 px-3 leading-8 transition-colors duration-200 ease-in-out">

                <label for="content" class="font-semibold">Content :</label>
                <textarea type="text" id="content" rows=3 bind:value="{content}"
                class="w-full bg-white rounded border border-gray-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 text-base outline-none text-gray-700 py-3 my-2 px-3 leading-8 transition-colors duration-200 ease-in-out" />
                
                <button class="text-white bg-indigo-500 border-0 py-2 px-6 focus:outline-none hover:bg-indigo-600 rounded text-lg">Change</button>
            </form>

        {/if}

    {:else}
        <Loading />
    {/if}
</div>



