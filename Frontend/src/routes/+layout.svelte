<script>
    import "../app.css"

    import { onMount } from "svelte";

    import jwt_decode from "jwt-decode";

    import { user, authTokens } from "$lib/stores";

	import Navbar from "./navbar.svelte";


    let mounted = false;


    const initUser  = async () => {
        let initTokens = null;
        let initUser = null;

        if (localStorage.getItem("authTokens") != null) {
            initTokens = JSON.parse(localStorage.getItem("authTokens"));
            initUser = jwt_decode(localStorage.getItem("authTokens"));
        }

        $authTokens = initTokens;
        $user = initUser;

    }

    

    onMount(async () => {
        await initUser();

        mounted = true;
    })
</script>

<head>
    <script src="https://kit.fontawesome.com/c8f4c629c9.js" crossorigin="anonymous"></script>
</head>

{#if mounted}
<Navbar />


<div class="w-3/4 mx-auto">
    <slot />
</div>
{/if}