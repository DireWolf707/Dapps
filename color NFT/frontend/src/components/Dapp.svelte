<script>
    import { onMount } from "svelte";
    import { selectedAccount,web3 } from 'svelte-web3';
    import { abi,address } from "../contract";
    import Loading from "./Loading.svelte";

    let contract;
    let loading=false;
    let colors;

    let value="";
    let info;
    let mint=false;
    
    onMount(()=>{
        contract = new $web3.eth.Contract(abi,address);
        getUserColors();
    })

    $:onValueChange(value);
    const onValueChange = async (_value)=>{
        if (checkRegex(_value)) {
            let exists = await contract.methods.colorExists(_value).call({from:$selectedAccount});
            if (!exists) {
                info = "Color Code Availabe!";
                mint = true;
            } else {
                info = "Color Code Unavailabe!";
                mint = false;
            }
        }
        else {
            info = "Must be a valid color code!";
            mint = false;
        }
    }

    $:onAccountChange($selectedAccount)
    const onAccountChange = ()=>{
        value=""
        getUserColors();
    }

    const checkRegex = (_string)=>{
        const regex = new RegExp("^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$");
        return regex.test(_string);
    }

    const getUserColors = async ()=>{
        colors = await contract.methods.getUserColors().call({from:$selectedAccount});
    }

    const mintHandler = async ()=>{
        try {
            loading = true;
            await contract.methods.mint(value).send({from:$selectedAccount});
        } catch (error) {
            console.log(error);
        } finally {
            value="";
            loading=false;
            colors=undefined;
            getUserColors();
        }
    }
</script>


<div class="w-1/3 mx-auto mt-4">

    {#if !loading}
        <div class="flex items-center justify-center">
            <div class="text-lg font-bold">
                Enter Color Code: &nbsp; 
            </div>
            <input type="text" class="border p-2 rounded" bind:value="{value}" placeholder="e.g. #FFFFFF">

            {#if mint}
                <button class="border px-2 py-1 bg-green-400 ml-2 rounded" on:click="{mintHandler}">
                    Mint
                </button>
            {/if}

        </div>
        
        <div class="flex justify-center text-lg" class:text-yellow-900={mint}>
            ({info})
        </div>
    {:else}
        <Loading />
    {/if}

</div>


<div class="w-4/5 mx-auto mt-10">
    <div class="text-2xl font-extrabold text-center mb-10">
        Your Colors
    </div>
    {#if colors}
        <div class="grid grid-cols-3 gap-4">
            {#each colors as color}
                <div>
                    <div class="bg-[{color}] rounded-full w-44 h-44 mx-auto"></div>
                    <div class="text-center mt-2 text-lg text-[{color}]"> {color} </div>
                </div>
            {/each}
        </div>
    {:else}
        <Loading value={"Loading"} yMargin={40} />
    {/if}
</div>