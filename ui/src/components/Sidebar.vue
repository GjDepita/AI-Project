<template>
    <aside class="w-64 bg-gray-900 text-gray-100 p-4">
        <img alt="Vue logo" class="logo mb-2" src="@/assets/logo.svg" width="40" height="40" />
        <hr class="mb-2" />
        <nav class="space-y-2">
            <RouterLink to=" " class="block p-2 rounded hover:bg-indigo-500 transition">Detect/Scan</RouterLink>
            <RouterLink to="/train-model" class="block p-2 rounded hover:bg-indigo-500 transition">Traning Model</RouterLink>
            <!-- <RouterLink to="/about" class="block p-2 rounded hover:bg-indigo-500 transition">About</RouterLink> -->
        </nav>
    </aside>
</template>
<!-- Sidebar -->