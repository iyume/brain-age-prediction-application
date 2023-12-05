<script setup lang="ts">
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://vuejs.org/api/sfc-script-setup.html#script-setup
import {
  NUpload,
  NUploadDragger,
  NText,
  NIcon,
  NButton,
  darkTheme,
  NConfigProvider,
  NNumberAnimation,
  NStatistic,
  StatisticProps,
  UploadFileInfo,
} from "naive-ui";
import { ArchiveOutline as ArchiveIcon } from "@vicons/ionicons5";
import { ref } from "vue";

const host = "http://127.0.0.1:8000";

const stat1Overrides: StatisticThemeOverrides = {
  labelFontSize: "14px",
  valueFontSize: "34px",
};

const thumbnail = ref<string | undefined>(undefined);

type StatisticThemeOverrides = NonNullable<StatisticProps["themeOverrides"]>;

function handleFinish({
  event,
}: {
  file: UploadFileInfo;
  event?: ProgressEvent;
}) {
  const resp = (event?.target as XMLHttpRequest).response;
  if (!resp) {
    console.warn("not receive response");
  }
  thumbnail.value = JSON.parse(resp).thumbnail;
}
</script>

<template>
  <n-config-provider :theme="darkTheme">
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

      <img
        :src="thumbnail ? `data:image/png;base64,${thumbnail}` : undefined"
        :hidden="thumbnail == undefined"
        width="100"
        height="100"
        style="margin: auto"
      />

      <div style="height: 48px; flex-shrink: 0"></div>

      <n-button type="primary" size="large" style="margin: auto"
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
            :to="80"
            :precision="2"
          />
          <template #suffix> 岁</template>
        </n-statistic>
      </div>

      <div style="flex-grow: 1"></div>

      <n-text>后端状态 {{ "🟢🔴" }}</n-text>
      <div style="height: 10%"></div>
    </div>
  </n-config-provider>
</template>
