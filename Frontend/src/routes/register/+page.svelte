<script>

    import { goto } from "$app/navigation";

    import { error, currentPage } from "$lib/stores";
    import url from "$lib/url";

    $currentPage = "Login"
    $error = null

    let username = '';
    let email = '';
    let password = '';
    let password2 = '';

    const registerUser = async () => {
        const response = await fetch(`${url}/auth/register/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username,
                email,
                password,
                password2
            })
        });

        if (response.status === 201) {
            goto("/login/")
        } else {
            let data = await response.json()
            $error = Object.values(data)[0]
        }
    };

</script>

<div class="flex justify-center items-center w-full min-h-screen">
    <form on:submit|preventDefault={registerUser} class="flex flex-col text-m items-center justify-center min-h-full w-1/5">
        <h1 class="font-extrabold text-5xl text-center mb-10">Login</h1>

        <label class="font-bold" for="username">Username</label>
        <input class="w-full mb-2 px-2 my-1 p-0.5 px-2 rounded-md border-2 border-gray-300 focus:border-black focus:outline-none" type="text" name="username" placeholder="jon.dough" bind:value={username} />

        <label class="font-bold" for="email">Email</label>
        <input class="w-full mb-2 px-2 my-1 p-0.5 px-2 rounded-md border-2 border-gray-300 focus:border-black focus:outline-none" type="text" name="email" placeholder="jon.dough@gmail.com" bind:value={email} />

        <label class="font-bold" for="password">Password</label>
        <input class="w-full mb-4 px-2 my-1 p-0.5 px-2 rounded-md border-2 border-gray-300 focus:border-black focus:outline-none" type="password" name="password" placeholder="**********" bind:value={password} />

        <label class="font-bold" for="password2">Confirm password</label>
        <input class="w-full mb-4 px-2 my-1 p-0.5 px-2 rounded-md border-2 border-gray-300 focus:border-black focus:outline-none" type="password" name="password2" placeholder="**********" bind:value={password2} />

        <button class="mt-2 border-gray-300 border hover:border-black btn rounded-md py-1 w-full my-2 font-extrabold text-l" type="submit">Submit</button>
    </form>
</div>