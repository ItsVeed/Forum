<script>
    import { onMount } from "svelte";

    import { baseUrl } from "$lib/url";
    import { user } from "$lib/stores";
    import useAxios from "$lib/api/useAxios";
    import errorCatch from "$lib/errorCatch";
    import url from "$lib/url";

    import dayjs from "dayjs";
    import { marked } from "marked";

    export let post;
    export let createComment;

    let owner = false;
    let liked = false;

    const scrollToCreateComment = () => {
        createComment.scrollIntoView();
    };

    const likePost = async () => {
        if ($user != null) {
            const api = useAxios();
            const response = await api.put(`${url}/forum/post/${post.pk}/like/`).catch(errorCatch);

            if (response.status == 200) {
                liked = !liked
                liked ? post.likes += 1 : post.likes -= 1
            }
            
        }
    }

    onMount(() => {
        if ($user != null) {
            liked = post.users_liked.includes($user.username)
            owner = post.user_serialized.username == $user.username
        }
    })
</script>

<div class="w-full mt-8 mb-4 flex flex-row min-h-64 border">
    <div class="bg-gray-200 w-2/12 flex flex-col justify-center items-center text-sm">
        <img class="mt-8 mb-4 w-24" src={baseUrl + post.user_serialized.profile_pic} alt="" />
        <h1 class="mb-4 text-3xl font-bold">{post.user_serialized.username}</h1>

        {#each post.user_serialized.roles_serialized as role}
        <div class="border-cyan-500 border-2 w-1/2 rounded-sm bg-white">
            <h2 class="text-xl px-2 py-0.5 text-center">{role.name}</h2>
        </div>
        {/each}

        <div class="flex flex-row justify-between w-full mt-4 px-12">
            <h2 class="text-gray-400">Posts</h2>
            <h2 class="text-end">{post.user_serialized.num_of_posts}</h2>
        </div>
        <div class="flex flex-row justify-between w-full px-12 pb-2">
            <h2 class="text-gray-400">Comments:</h2>
            <h2 class="text-end">{post.user_serialized.num_of_comments}</h2>
        </div>
    </div>

    <div class="flex flex-col w-10/12">
        <h1 class="text-start mx-auto p-1 border-b border-gray-200 w-11/12 text-m text-gray-400">{dayjs(post.datetimeuploaded).format("MMMM, D YYYY").toString()}</h1>

        <div class="w-11/12 py-2 mx-auto grow">
            {@html marked(post.post)}
        </div>

        <div class="flex flex-row justify-end p-2 items-center">
            <h2 class="text-xs pr-1 font-bold">{post.likes}</h2>
            <i on:click={likePost} on:keypress class="{liked ? "fa-solid" : "fa-regular"} hover:text-gray-400 fa-heart"></i>
            <i class="px-4 hover:text-gray-400 fa-regular fa-comment" on:click={scrollToCreateComment} on:keypress></i>
        </div>
    </div>
    
</div>