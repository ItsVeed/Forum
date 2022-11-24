<script>
    import { onMount, createEventDispatcher } from "svelte";

    import { baseUrl } from "$lib/url";
    import { user } from "$lib/stores";
    import useAxios from "$lib/api/useAxios";
    import errorCatch from "$lib/errorCatch";
    import url from "$lib/url";

    export let post;

    let show = false;
    let userInfo;

    let comment = "";

    const dispatch = createEventDispatcher();

    const createComment = () => {
        const api = useAxios();
        api.post(`${url}/forum/comment/create/`, {
            comment,
            post,
        }).catch(errorCatch);

        dispatch('message', {
            text: 'updatePosts'
        })

        comment = "";
    }

    const fetchUserInfo = async () => {
        const api = useAxios();
        const response = await api.get(`${url}/forum/user/${$user.username}/`).catch(errorCatch);
        userInfo = response.data;
    }

    onMount(() => {
        if ($user != null) {
            fetchUserInfo();
            show = true;
        }

        
    })

</script>

{#if show && userInfo}

<div class="w-full mb-4 flex flex-row min-h-64 border">
    <div class="bg-gray-200 w-2/12 flex flex-col justify-center items-center text-sm">
        <img class="mt-8 mb-4 w-24" src={userInfo.profile_pic} alt="" />
        <h1 class="mb-4 text-3xl font-bold">{userInfo.username}</h1>

        {#each userInfo.roles_serialized as role}
        <div class="border-cyan-500 border-2 w-1/2 rounded-sm bg-white">
            <h2 class="text-xl px-2 py-0.5 text-center">{role.name}</h2>
        </div>
        {/each}

        <div class="flex flex-row justify-between w-full mt-4 px-12">
            <h2 class="text-gray-400">Posts</h2>
            <h2 class="text-end">{userInfo.num_of_posts}</h2>
        </div>
        <div class="flex flex-row justify-between w-full px-12 pb-2">
            <h2 class="text-gray-400">Comments:</h2>
            <h2 class="text-end">{userInfo.num_of_comments}</h2>
        </div>
    </div>

    <div class="flex flex-col w-10/12">
        <h1 class="text-start mx-auto p-1 border-b border-gray-200 w-11/12 text-m text-gray-400">New Comment</h1>

        <div class="w-11/12 py-2 mx-auto grow">
            <textarea class="text-m w-full h-40 focus:outline-none" bind:value={comment} />
        </div>

        <div class="flex flex-row justify-end p-2 items-center">
            <button on:click={createComment} class="mt-2 border-gray-300 border hover:border-black btn rounded-md py-1 w-1/6 my-2 font-extrabold text-l">Post</button>
        </div>
    </div>
    
</div>

{/if}