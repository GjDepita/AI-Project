<template>
  <div class="bg-gray-700 p-4 rounded text-white" v-if="ocrResult || croppedImage">
    <div v-if="croppedImage">
      <h3 class="font-bold mb-2">🖼️ Cropped Image</h3>
      <img :src="croppedImage" class="border mt-2 max-w-full" style="width: 100%; max-width: 300px;" />
    </div>

    <div v-if="ocrResult">
      <h3 class="font-bold mt-4 mb-2">🔍 Detected Serial Numbers</h3>
      <ul class="list-disc pl-5">
        <li v-for="serial in ocrResult.serials" :key="serial">{{ serial }}</li>
      </ul>

      <!-- <h4 class="font-semibold mt-4">📃 Raw OCR Output</h4>
      <ul class="list-disc pl-5">
        <li v-for="text in ocrResult.raw_ocr" :key="text">{{ text }}</li>
      </ul> -->
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from "vue";

const props = defineProps({
  croppedImage: String,
});

const ocrResult = ref(null);

// 🔁 Watch for changes in croppedImage and trigger upload
watch(
  () => props.croppedImage,
  (newImg) => {
    if (newImg) {
      uploadToFastAPI(newImg);
    }
  }
);

async function uploadToFastAPI(base64Image) {
  const blob = base64ToBlob(base64Image);
  const formData = new FormData();
  formData.append("file", blob, "cropped.jpg");

  try {
    const res = await fetch("http://localhost:8001/detect/", {
      method: "POST",
      body: formData,
    });
    const data = await res.json();
    ocrResult.value = data;
  } catch (err) {
    console.error("Error uploading:", err);
  }
}

// 🧠 Helper: Convert base64 image to blob
function base64ToBlob(base64) {
  const byteString = atob(base64.split(",")[1]);
  const mimeString = base64.split(",")[0].split(":")[1].split(";")[0];

  const ab = new ArrayBuffer(byteString.length);
  const ia = new Uint8Array(ab);
  for (let i = 0; i < byteString.length; i++) {
    ia[i] = byteString.charCodeAt(i);
  }

  return new Blob([ab], { type: mimeString });
}
</script>

<style scoped>
/* You can also add Tailwind's dark:bg-... if you're using dark mode utility classes */
</style>
