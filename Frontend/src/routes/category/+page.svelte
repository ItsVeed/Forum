<script>

    import { onMount } from "svelte";
    import { page } from "$app/stores"

    import useAxios from "$lib/api/useAxios";
    import errorCatch from "$lib/errorCatch";
    import url from "$lib/url";
    
    import PostListComp from "$lib/components/PostListComp.svelte";

    const pk = $page.params.pk;

    let category;
    let posts;
    let pinnedPosts;

    let mounted = false;

    const getCategory = async () => {
        const api = useAxios();
        const response = await api.get(`${url}/forum/category/${pk}/`).catch(errorCatch);

        category = response.data
        posts = category.posts.filter(e => e.pinned == false)
        pinnedPosts = category.posts.filter(e => e.pinned == true)
    }

    onMount(async () => {
        await getCategory();

        mounted = true;
    })

</script>

{#if mounted}
    <div class="mx-auto w-3/4 mt-4">
        <div class="flex flex-row items-center justify-between pb-4">
            <p class="text-sm mb-4">{`Home > Forums > ${category.section_name} > ${category.name}`}</p>
            <a href={`/post/create/${category.pk}/`}><i class="text-gray-400 hover:text-gray-300 fa-solid fa-plus fa-xl"></i></a>
        </div>
        
        <h1 class="rounded-sm bg-gray-300 p-2">Pinned posts</h1>
        {#each pinnedPosts as post}
            <PostListComp post={post} border={pinnedPosts.indexOf(post) != pinnedPosts.length - 1} />
        {/each}

        <h1 class="rounded-sm bg-gray-300 p-2 mt-4">Posts</h1>
        {#each posts as post}
            <PostListComp post={post} border={posts.indexOf(post) != posts.length - 1} />
        {/each}

    </div>
{/if}