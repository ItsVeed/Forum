<script>

    import { goto } from "$app/navigation";

    import jwt_decode from "jwt-decode";

    import { user, authTokens, error, currentPage } from "$lib/stores";
    import url from "$lib/url";

    $currentPage = "Login"
    $error = null

    let username = '';
    let password = '';

    const loginUser = async () => {
        const response = await fetch(`${url}/auth/login/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username,
                password
            })
        });
        const data = await response.json();

        if (response.status === 200) {
            $authTokens = data;
            $user = jwt_decode(data.access);
            localStorage.setItem("authTokens", JSON.stringify(data));
            goto("/");
        } else {
            alert("Something went wrong!")
        }
    };

</script>

<div class="flex justify-center items-center w-full min-h-screen">
    <form on:submit|preventDefault={loginUser} class="flex flex-col text-m items-center justify-center min-h-full w-1/5">
        <h1 class="font-extrabold text-5xl text-center mb-10">Login</h1>

        <label class="font-bold" for="username">Username</label>
        <input class="w-full mb-2 px-2 my-1 p-0.5 px-2 rounded-md border-2 border-gray-300 focus:border-black focus:outline-none" type="text" name="username" placeholder="jon.dough" bind:value={username} />

        <label class="font-bold" for="password">Password</label>
        <input class="w-full mb-4 px-2 my-1 p-0.5 px-2 rounded-md border-2 border-gray-300 focus:border-black focus:outline-none" type="password" name="password" placeholder="**********" bind:value={password} />

        <button class="mt-2 border-gray-300 border hover:border-black btn rounded-md py-1 w-full my-2 font-extrabold text-l" type="submit">Submit</button>
    </form>
</div>