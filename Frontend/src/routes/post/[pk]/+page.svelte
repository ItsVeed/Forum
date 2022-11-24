<script>
    import { onMount } from "svelte";
    import { page } from "$app/stores";
    import { goto } from "$app/navigation";

    import dayjs from "dayjs";

    import useAxios from "$lib/api/useAxios";
    import errorCatch from "$lib/errorCatch";
    import url from "$lib/url";
    import { user } from "$lib/stores";

    import PostComp from "$lib/components/PostComp.svelte";
    import CommentComp from "$lib/components/CommentComp.svelte";
	import NewCommentComp from "$lib/components/NewCommentComp.svelte";

    const post_id = $page.params.pk

    let post;
    let owner = false;

    let mounted = false;

    let createComment;

    const getPost = async () => {
        const api = useAxios();
        const response = await api.get(`${url}/forum/post/${post_id}/`).catch(errorCatch);

        post = response.data
    }

    const deletePost = () => {
        const api = useAxios();
        const response = api.delete(`${url}/forum/post/${post_id}/delete/`).catch(errorCatch);
        goto(`/category/${post.category}/`)
    }

    onMount(async () => {
        await getPost();

        if ($user != null) {
            owner = post.user_serialized.username == $user.username
        }

        mounted = true;
    })

</script>

{#if mounted}
<div class="flex flex-row pt-4 items-center">
    <div class="flex flex-col justify-between w-full">
        <h1 class="text-2xl font-bold">{post.title}</h1>
        <div class="flex flex-row">
            <a href={`/profile/${post.user_serialized.pk}/`}><h2 class="hover:underline">{post.user_serialized.username}</h2></a>
            <h2 class="mx-2">.</h2>
            <h2 class="text-gray-400">{dayjs(post.datetimeuploaded).format("MMMM, D YYYY").toString()}</h2>
        </div>
    </div>
    {#if owner}
    <i class="hover:text-gray-400 fa-solid fa-trash fa-2xl" on:click={deletePost} on:keypress></i>
    {/if}
    
</div>

<PostComp post={post} createComment={createComment} />

{#each post.comments as comment}
    <CommentComp comment={comment} on:message={getPost} />
{/each}


<NewCommentComp post={post.pk} on:message={getPost}/>
<div bind:this={createComment}></div>

{/if}