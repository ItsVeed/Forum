<script>

    import { onMount } from "svelte";

    import url from "$lib/url";
    import CategoryListComp from "$lib/components/CategoryListComp.svelte";
    import InfoBox from "$lib/components/InfoBox.svelte";
    import useAxios from "$lib/api/useAxios";
    import errorCatch from "$lib/errorCatch";

    let mounted = false;
    let sections = null;

    const getSections = async () => {
        
    }

    onMount(async () => {
        const api = useAxios();
        const response = await api.get(`${url}/forum/sections/`).catch(errorCatch);

        sections = response.data;

        mounted = true;
    })

</script>

{#if sections != null}
<div class="flex flex-row">
    <div class="w-4/6 min-h-screen mx-2 my-4">
        {#each sections as section}
            <h1 class="w-full p-2 rounded-sm bg-gray-300">{section.name}</h1>
            {#each section.categories as category}
                <CategoryListComp category={category} />
            {/each}
        {/each}
    </div>
    <div class="w-2/6 min-h-screen">
        <InfoBox />
    </div>
</div>
{/if}
