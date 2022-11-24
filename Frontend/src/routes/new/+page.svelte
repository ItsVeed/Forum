<script>

    import { onMount } from "svelte";

    import useAxios from "$lib/api/useAxios";
    import errorCatch from "$lib/errorCatch";
    import url from "$lib/url";
    import PostListComp from "$lib/components/PostListComp.svelte";

    let posts;

    let mounted = false;

    const getPosts = async () => {
        const api = useAxios();
        const response = await api.get(`${url}/forum/posts/`).catch(errorCatch);

        posts = response.data
    }

    onMount(async () => {
        await getPosts();

        mounted = true;
    })

</script>

{#if mounted}
    <div class="mx-auto w-3/4 mt-4">
        <h1 class="rounded-sm bg-gray-300 p-2 mt-8">New Posts</h1>
        {#each posts as post}
            <PostListComp post={post} border={posts.indexOf(post) != posts.length - 1} />
        {/each}

    </div>
{/if}