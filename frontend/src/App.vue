<script setup lang="ts">
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://vuejs.org/api/sfc-script-setup.html#script-setup
import {
  NUpload,
  NUploadDragger,
  NText,
  NIcon,
  NButton,
  lightTheme,
  darkTheme,
  NConfigProvider,
  NNumberAnimation,
  NStatistic,
  StatisticProps,
  UploadFileInfo,
} from "naive-ui";
import {
  ArchiveOutline as ArchiveIcon,
  CloseOutline as CloseIcon,
  CheckmarkOutline as CheckIcon,
} from "@vicons/ionicons5";
import { usePreferredColorScheme } from "@vueuse/core";
import { ref, computed } from "vue";

const host = "http://127.0.0.1:8000";

const stat1Overrides: StatisticThemeOverrides = {
  labelFontSize: "14px",
  valueFontSize: "34px",
};

type UploadRespJson = {
  file_id: string;
  thumbnail: string; // base64 string
};
const currentFile = ref<UploadRespJson | undefined>(undefined);

const predictLoading = ref<boolean>(false);
const predictResult = ref<number | null>(null);

type StatisticThemeOverrides = NonNullable<StatisticProps["themeOverrides"]>;

const preferredColor = usePreferredColorScheme();
const preferredTheme = computed(
  () =>
    ({ light: lightTheme, dark: darkTheme, "no-preference": lightTheme }[
      preferredColor.value
    ])
);

const serverStatus = ref<boolean>(false);
// get once
(() => {
  let req = new XMLHttpRequest();
  req.open("GET", `${host}/ping`, true);
  req.onload = () => {
    if (req.status == 200) {
      serverStatus.value = true;
    }
  };
  req.send();
})();

function handleFinish(options: {
  file: UploadFileInfo;
  event?: ProgressEvent;
}) {
  const resp = (options.event?.target as XMLHttpRequest).response;
  if (!resp) {
    console.warn("not receive response");
  }
  const resp_json: UploadRespJson = JSON.parse(resp);
  currentFile.value = resp_json;
  return options.file;
}

function handleRemove(options: {
  file: UploadFileInfo;
  fileList: Array<UploadFileInfo>;
}) {
  options;
  currentFile.value = undefined;
  return true;
}

function handlePredict() {
  const file_id = currentFile.value?.file_id;
  if (!file_id) {
    return;
  }
  predictLoading.value = true;
  let req = new XMLHttpRequest();
  req.open("POST", `${host}/evaluate`, true);
  req.setRequestHeader("Content-Type", "application/json");
  req.onload = () => {
    if (req.status == 200) {
      predictResult.value = JSON.parse(req.response).result;
    }
    predictLoading.value = false;
  };
  const data = JSON.stringify({ file_id });
  req.send(data);
}
</script>

<template>
  <n-config-provider :theme="preferredTheme">
    <div class="container">
      <div style="height: 10%"></div>

      <n-text style="margin-bottom: 6px; font-size: 32px"
        >大脑 MRI 年龄预测</n-text
      >
      <n-text style="margin: 8px auto; font-size: 16px">
        Brain MRI Age Prediction using Resnet Bottleneck
      </n-text>

      <div style="height: 32px"></div>

      <n-upload
        accept=".nii"
        :action="`${host}/get_thumbnail`"
        @finish="handleFinish"
        @remove="handleRemove"
        :max="1"
        style="width: 60%; margin: auto"
      >
        <n-upload-dragger>
          <div style="margin-bottom: 12px">
            <n-icon size="48" :depth="3">
              <archive-icon />
            </n-icon>
          </div>
          <n-text style="font-size: 16px">
            点击或者拖动文件到该区域来上传
          </n-text>
        </n-upload-dragger>
      </n-upload>

      <n-text :hidden="currentFile == undefined">上传成功！</n-text>
      <img
        :src="
          currentFile
            ? `data:image/png;base64,${currentFile.thumbnail}`
            : undefined
        "
        :hidden="currentFile == undefined"
        width="100"
        height="100"
        alt="MRI 缩略图"
        style="margin: auto"
      />

      <div style="height: 24px; flex-shrink: 0"></div>

      <n-button
        type="primary"
        size="large"
        style="margin: auto"
        @click="handlePredict"
        :loading="predictLoading"
        >预测年龄</n-button
      >

      <div style="margin: 40px auto">
        <n-statistic
          label="你的预测年龄是"
          tabular-nums
          :theme-overrides="stat1Overrides"
        >
          <n-number-animation
            ref="numberAnimationInstRef"
            :from="0"
            :to="predictResult || 0"
            :precision="2"
          />
          <template #suffix> 岁</template>
        </n-statistic>
      </div>

      <div style="flex-grow: 1"></div>

      <n-text style="align-self: center; display: flex; align-items: center">
        后端状态
        <check-icon
          v-if="serverStatus"
          style="color: #08b45f; margin-left: 4px; width: 30px; height: 30px"
        />
        <close-icon
          v-else
          style="color: #d3302e; margin-left: 4px; width: 30px; height: 30px"
        />
      </n-text>
      <div style="height: 10%"></div>
    </div>
  </n-config-provider>
</template>
