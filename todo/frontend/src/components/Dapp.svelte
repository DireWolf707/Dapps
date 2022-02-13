<script>
    import { onMount } from "svelte";
    import { selectedAccount,web3 } from 'svelte-web3';
    import { abi,address } from "../contract";

    let contract;

    let loading=false;
    let updating=false;
    let update_id=-1;

    let tasks=[];
    let newTask="";

    $: onAccountChange($selectedAccount);
    const onAccountChange = async()=>{
        if (contract) {
            getTasks();
        }
    }

    onMount(async()=>{
        contract = new $web3.eth.Contract(abi,address);
        getTasks();
    })

    const getTasks = async ()=>{
        let _tasks = await contract.methods.getTasks().call({
                from:$selectedAccount
        });
        tasks = Array.from(_tasks)
    }

    const createTask = async ()=>{
        loading=true;
        try {
            if (!updating) {
                await contract.methods.createTask(newTask).send({
                    from:$selectedAccount
                });
            } else {
                await contract.methods.changeContent(update_id,newTask).send({
                    from:$selectedAccount
                });
            }
        } catch (error) {
            console.log(error);
        } finally {
            if (updating) {
                updating=false;
                update_id=-1;
            }
            getTasks();
            newTask="";
            loading=false;
        }
    }

    const changeCompleted = async (_id)=>{
        loading=true;
        try {
            await contract.methods.changeCompleted(_id).send({
                from:$selectedAccount
            });
        } catch (error) {
            console.log(error);
        } finally {
            getTasks();
            loading=false;
        }
    }

    const changeContent = async (_id,_content)=>{
        updating=true;
        update_id=_id;
        newTask=_content;
    }

</script>


<div class="w-1/2 mx-auto mt-8 py-4 px-8">

    
        {#if !loading}
            <div class="bg-gray-200 flex justify-between p-2 rounded">

                <input type="text" bind:value="{newTask}" class="w-2/3 border rounded px-1 py-2">
                <button on:click="{createTask}" class="w-1/3 bg-violet-400 hover:bg-red-400 text-white p-2 ml-3 rounded">
                {#if !updating}
                    Create Task
                {:else}
                    Update Task
                {/if}
                </button>

            </div>
        {:else}
            <div class="text-xl flex justify-center">transaction... &nbsp;
                <svg role="status" class="mr-2 w-8 h-8 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="currentColor"/>
                    <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentFill"/>
                </svg>
            </div>
        {/if}

    <div class="grid grid-cols-1 text-xl mt-2">
    {#each tasks as task,id}
        <div class="flex justify-between m-1">
            <div class="flex item-center">
                <input type="checkbox" bind:checked="{tasks[id].completed}" style="width: 15px;height: 30px;"
                on:click="{()=>{changeCompleted(id)}}">
                <div class:line-through={tasks[id].completed} class="ml-1">{task.content}</div>
            </div>
            
            <button class="bg-yellow-300 hover:bg-yellow-500 text-white py-1 px-2 rounded"
            on:click="{()=>changeContent(id,task.content)}">update</button>
        </div>
    {/each}
    </div>

    
</div>

<style></style>