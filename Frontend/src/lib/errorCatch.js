import { goto } from "$app/navigation";

import { error } from "$lib/stores";

const catchError = (err) => {
    if (err.response.status === 401 | err.response.status === 403) {
        goto('/unauthorized/');
    } else {
        error.set(err.response.data);
    }
}

export default catchError