import { writable } from "svelte/store";

export const user = writable(null);

export const authTokens = writable(null);

export const currentPage = writable(null);

export const error = writable(null);

export const term = writable(null);