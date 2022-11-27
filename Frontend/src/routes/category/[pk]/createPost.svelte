<script>
    import { createEventDispatcher } from "svelte";

    import useAxios from "$lib/api/useAxios";
    import errorCatch from "$lib/errorCatch";
    import url from "$lib/url";

    export let category;

    let title = "";
    let post = "";

    const dispatch = createEventDispatcher();

    const close = () => {
        dispatch('message', {
            text: 'close'
        })
    }

    export const createPost = async () => {
        if (title != "" && post != "") {
            console.log("test")
            const api = useAxios();
            const response = await api.post(`${url}/forum/post/create/`, {
                category,
                title,
                post,
            }).catch(errorCatch);

            if (response) {
                close();
            }

        }
    }
</script>

<div class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full" />

<div
	class="absolute top-20 mx-auto p-3 border w-5/6 shadow-lg rounded-md bg-white"
>
	<div class="text-center flex flex-col">
        <button on:click={close} class="justify-self-end self-end p-1"><i class="fa-solid fa-xmark"></i></button>

        <label for="title">Title</label>
        <input class="w-full mb-2 px-2 my-1 p-0.5 px-2 rounded-sm border-2 border-gray-300 focus:border-black focus:outline-none" type="text" name="title" bind:value={title}>

        <label for="post">Discussion</label>
        <textarea class="w-full h-96 mb-2 px-2 my-1 p-0.5 px-2 rounded-sm border-2 border-gray-300 focus:border-black focus:outline-none" name="post" bind:value={post} />

        <button class="self-center mt-2 border-gray-300 border hover:border-black btn rounded-md py-1 w-1/3 my-2 font-extrabold text-l" on:click={createPost}>Post</button>
	</div>
</div>