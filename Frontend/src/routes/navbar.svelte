<script>

    import { onMount } from "svelte";
    import { goto } from "$app/navigation";

    import { user, authTokens, term } from "$lib/stores";

    import useAxios from "$lib/api/useAxios";
    import url from "$lib/url";
    import errorCatch from "$lib/errorCatch";

    let searchTerm = "";
    let userInfo = null;

    let mounted = false;

    const fetchUserInfo = async () => {
        const api = useAxios();
        const response = await api.get(url + `/forum/user/${$user.username}/`).catch(errorCatch);
        userInfo = response.data;
    }

    const logoutUser = () => {
        $authTokens = null;
        $user = null;
        localStorage.removeItem("authTokens");
    }

    const search = () => {
        $term = searchTerm
        goto(`/post/search/`)
    }

    onMount(async () => {
        if ($user) await fetchUserInfo();

        mounted = true;
    })


</script>

<header class="sticky to-0 z-50">
    <nav class=" flex justify-between items-center text-lg px-4 py-1 bg-gray-300 w-full h-16">
        <div class="flex flex-row items-center gap-10">
            <h1 class="text-2xl font-bold">Tori's services</h1>
            <a href="/">Forums</a>
            <a href="/new/">What's new</a>
            <form on:submit|preventDefault={search}>
                <input class="rounded-sm p-1 h-8 w-64 {searchTerm.length > 0 ? "text-start" : "text-center"} focus:outline-none" type="text" placeholder="search" bind:value={searchTerm} />
            </form>
        </div>
        <div class="flex flex-row items-center gap-10">
            {#if $user && userInfo}
                <a class="w-8" href={`/profile/${$user.username}/`}><img src={userInfo.profile_pic} alt={userInfo.username} /></a>
                <a href="/" on:click={logoutUser}>Logout</a>
            {:else}
                <a href="/login/">Login</a>
                <a href="/register/">Register</a>
            {/if}
        </div>
    </nav>
</header>