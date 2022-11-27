<script>
    import { onMount } from "svelte";

    import useAxios from "$lib/api/useAxios";
    import errorCatch from "$lib/errorCatch";
    import url from "$lib/url";
    import { baseUrl } from "$lib/url";

    import dayjs from "dayjs";

    let stats;
    let posts;

    let mounted = false;

    const getStats = async () => {
        const api = useAxios();
        const response = await api.get(`${url}/forum/stats/`).catch(errorCatch)

        stats = response.data
    }

    const getPosts = async () => {
        const api = useAxios();
        const response = await api.get(`${url}/forum/posts/`).catch(errorCatch)

        posts = response.data.slice(0, 4)

        console.log(posts)
    }

    onMount(async () => {
        await getPosts();
        await getStats();

        mounted = true;
    })
</script>

{#if mounted}
<div class="w-full mt-4 ml-2 border rounded-sm text-m">
    <h1 class="w-full p-2 bg-gray-300 text-lg font-bold">Latest posts</h1>
    <div class="my-4">
        {#each posts as post}
            <div class="m-4 flex flex-row items-center border-b py-3">
                <a href={`/post/${post.pk}/`}><img class="w-14" src={baseUrl + post.user_serialized.profile_pic} alt="" /></a>
                <div class="flex flex-col ml-20">
                    <a href={`/post/${post.pk}/`}><h1 class="text-lg font-semibold hover:underline">{post.title}</h1></a>
                    <div class="flex flex-row text-sm">
                        <a href={`/profile/${post.user_serialized.username}`}><h2 class="hover:underline">{post.user_serialized.username}</h2></a>
                        <h2 class="mx-2">.</h2>
                        <h2 class="text-gray-400">{dayjs(post.datetimeuploaded).format("MMMM, D YYYY").toString()}</h2>
                    </div>
                </div>
            </div>
        {/each}
    </div>

    <h1 class="w-full bg-gray-300 p-2 text-lg font-bold">Forum stats</h1>
    <div class="p-4">
        <div class="flex flex-row justify-between">
            <h2 class="text-gray-400">Posts:</h2>
            <h2 class="text-end">{stats.post_count}</h2>
        </div>
        <div class="flex flex-row justify-between">
            <h2 class="text-gray-400">Comments:</h2>
            <h2 class="text-end">{stats.comment_count}</h2>
        </div>
        <div class="flex flex-row justify-between">
            <h2 class="text-gray-400">Users:</h2>
            <h2 class="text-end">{stats.user_count}</h2>
        </div>
        <div class="flex flex-row justify-between">
            <h2 class="text-gray-400">Latest user:</h2>
            <h2 class="text-end">{stats.latest_user.username}</h2>
        </div>
    </div>
    
</div>
{/if}