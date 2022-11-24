<script>
    import { onMount, createEventDispatcher } from "svelte";

    import { baseUrl } from "$lib/url";
    import { user } from "$lib/stores";
    import useAxios from "$lib/api/useAxios";
    import errorCatch from "$lib/errorCatch";
    import url from "$lib/url";

    import dayjs from "dayjs";
    import { marked } from "marked";

    export let comment;

    let liked = false;
    let owner = false;

    const likeComment = async () => {
        if ($user != null) {
            const api = useAxios();
            const response = await api.put(`${url}/forum/comment/${comment.pk}/like/`).catch(errorCatch);

            if (response.status == 200) {
                liked = !liked
                liked ? comment.likes += 1 : comment.likes -= 1
            }
            
        }
    }

    const dispatch = createEventDispatcher();

    const deleteComment = () => {
        const api = useAxios();
        api.delete(`${url}/forum/comment/${comment.pk}/delete/`).catch(errorCatch);

        dispatch('message', {
            text: 'updatePosts'
        })
    }

    onMount(() => {
        if ($user != null) {
            owner = comment.user_serialized.username == $user.username
            liked = comment.users_liked.includes($user.username)
        }
    })

</script>

<div class="w-full mb-4 flex flex-row min-h-64 border">
    <div class="bg-gray-200 w-2/12 flex flex-col justify-center items-center text-sm">
        <img class="mt-8 mb-4 w-24" src={baseUrl + comment.user_serialized.profile_pic} alt="" />
        <h1 class="mb-4 text-3xl font-bold">{comment.user_serialized.username}</h1>

        {#each comment.user_serialized.roles_serialized as role}
        <div class="border-cyan-500 border-2 w-1/2 rounded-sm bg-white">
            <h2 class="text-xl px-2 py-0.5 text-center">{role.name}</h2>
        </div>
        {/each}

        <div class="flex flex-row justify-between w-full mt-4 px-12">
            <h2 class="text-gray-400">Posts</h2>
            <h2 class="text-end">{comment.user_serialized.num_of_posts}</h2>
        </div>
        <div class="flex flex-row justify-between w-full px-12 pb-2">
            <h2 class="text-gray-400">Comments:</h2>
            <h2 class="text-end">{comment.user_serialized.num_of_comments}</h2>
        </div>
    </div>

    <div class="flex flex-col w-10/12">
        <div class="flex flex-row mx-auto w-11/12 border-b border-gray-200 justify-between items-center">
            <h1 class="text-start p-1 w-3/4 text-m text-gray-400">{dayjs(comment.datetimeuploaded).format("MMMM, D YYYY").toString()}</h1>
            <i class="hover:text-gray-400 fa-solid fa-trash fa-sm" on:click={deleteComment} on:keypress></i>
        </div>
        
        <div class="w-11/12 py-2 mx-auto grow">
            {@html marked(comment.comment)}
        </div>

        <div class="flex flex-row justify-end p-2 items-center">
            <h2 class="text-xs pr-1 font-bold">{comment.likes}</h2>
            <i on:click={likeComment} on:keypress class="{liked ? "fa-solid" : "fa-regular"} pr-4 hover:text-gray-400 fa-heart"></i>
        </div>
    </div>
    
</div>