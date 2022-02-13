<script>
    import { selectedAccount } from 'svelte-web3';
    import PostDetail from "./PostDetail.svelte";

    export let contract;
    let posts=[];
    
    $:onAccountchanage($selectedAccount)
    const onAccountchanage = async() => {
        getPosts()
    }

    const getPosts = async() => {
        posts = await contract.methods.getPosts().call({from:$selectedAccount});
    }
</script>

<div class="w-2/5 mx-auto">
    {#each posts as post,id}
        <PostDetail {post} {id} {contract} />
    {/each}
</div>