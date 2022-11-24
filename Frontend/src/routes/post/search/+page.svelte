<script>

    import { onMount } from "svelte";

    import useAxios from "$lib/api/useAxios";
    import errorCatch from "$lib/errorCatch";
    import url from "$lib/url";
    import { term } from "$lib/stores";
    import PostListComp from "$lib/components/PostListComp.svelte";

    let posts;

    let mounted = false;

    const search = async () => {
        const api = useAxios();
        const response = await api.get(`${url}/forum/post/search/${$term}/`).catch(errorCatch);

        posts = response.data
    }

    onMount(async () => {
        await search();

        mounted = true;
    })

</script>

{#if mounted}
    <div class="mx-auto w-3/4 mt-4">
        <h1 class="rounded-sm bg-gray-300 p-2 mt-8">Results</h1>
        {#each posts as post}
            <PostListComp post={post} border={posts.indexOf(post) != posts.length - 1} />
        {/each}

    </div>
{/if}