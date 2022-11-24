<script>
    import { goto } from "$app/navigation";

    import url from "$lib/url";
    import errorCatch from "$lib/errorCatch";
    import useAxios from "$lib/api/useAxios";
    import { baseUrl } from "$lib/url";

    import dayjs from "dayjs";

    export let post;
    export let border;

    const deletePost = async () => {
        const api = useAxios();
        const response = api.delete(`${url}/forum/post/${post.pk}/delete/`).catch(errorCatch(err))
    }

    const gotoUser = () => {
        goto(`/profile/${post.user}/`)
    }
</script>

<div class="flex flex-row hover items-center h-24 w-full justify-between border-gray-300 {border ? 'border-b' : ''}">
    <div class="flex flex-row items-center">
        <a href={`/post/${post.pk}/`}><img class="w-12" src={baseUrl + post.user_serialized.profile_pic} alt="" /></a>
        <div class="flex flex-col justify-center ml-16">
            <a href={`/post/${post.pk}/`}><h1 class="text-xl font-semibold hover:underline">{post.title}</h1></a>
            <div class="flex flex-row text-sm">
                <a href={`/profile/${post.user_serialized.pk}/`}><h2 class="hover:underline">{post.user_serialized.username}</h2></a>
                <h2 class="mx-2">.</h2>
                <h2 class="text-gray-400">{dayjs(post.datetimeuploaded).format("MMMM, D YYYY").toString()}</h2>
            </div>
        </div>
    </div>
    
    <div class="flex flex-row items-center justify-end text-m">
        <div class="flex flex-col justify-center items-center">
            <h1 class="text-gray-400">Likes</h1>
            <h1>{post.likes}</h1>
        </div>
        <div class="flex flex-col justify-center items-center ml-8 mr-10">
            <h1 class="text-gray-400">Comments</h1>
            <h1>{post.comment_count}</h1>
        </div>
    </div>
</div>