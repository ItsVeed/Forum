<script>
    import dayjs from "dayjs";

    import { baseUrl } from "$lib/url";

    export let category;

    console.log(category)
</script>

<div class="flex flex-row h-24 w-full justify-between">
    <div class="flex flex-row items-center">
        <i class="fa-regular fa-comments"></i>
        <a href={`/category/${category.pk}/`}><h1 class="ml-2 text-xl hover:underline">{category.name}</h1></a>
    </div>
    
    <div class="flex flex-row items-center justify-end text-m">
        <div class="flex flex-col justify-center items-center">
            <h1 class="text-gray-400">Posts</h1>
            <h1>{category.post_count}</h1>
        </div>
        <div class="flex flex-col justify-center items-center ml-4 mr-10">
            <h1 class="text-gray-400">Comments</h1>
            <h1>{category.comment_count}</h1>
        </div>

        {#if category.latest_post.title != ""}
        <a href={`/post/${category.latest_post.pk}/`}><img class="w-8 m-2" src={baseUrl + category.latest_post.user_serialized.profile_pic} alt=""/></a>
        <div class="ml-2 mr-4">
            <a href={`/post/${category.latest_post.pk}/`}><h1>{category.latest_post.title}</h1></a>
            <h1 class="text-m text-gray-400">{dayjs(category.latest_post.datetimeuploaded).format("MMMM, D YYYY").toString()}</h1>
        </div>
        {:else}
            <div class="mr-3 w-48"></div>
        {/if}
    </div>
</div>