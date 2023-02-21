
<template>
  <lay-layout class="example">
    <lay-header>Fake ChatGPT</lay-header>
    <lay-body>
      <lay-scroll
        height="100%"
        width="100%"
        style="background-color: whitesmoke"
        thumbColor="#000000"
      >
        <lay-container>
          <lay-row>
            <lay-col span="24">
              <lay-panel
                v-for="(n, index) in result"
                :key="index"
                style="margin: 10px; padding: 10px"
                v-html="n"
              ></lay-panel>
            </lay-col>
          </lay-row>
        </lay-container>
      </lay-scroll>
    </lay-body>
    <lay-footer>
      <lay-row space="0">
        <lay-col xs="21" sm="21">
          <lay-input
            class="h-16"
            v-model="question"
            allow-clear="true"
            size="sm"
            @keyup.enter="clickHandle"
          ></lay-input>
        </lay-col>

        <lay-col xs="3" sm="3">
          <lay-button
            size="sm"
            class="h-16"
            type="normal"
            @click="clickHandle"
            :loading="loadState"
            loadingIcon="layui-icon-loading"
            >发送</lay-button
          ></lay-col
        >
      </lay-row>
    </lay-footer>
  </lay-layout>
</template>
<script setup>
import { ref } from "vue";
import dayjs from "dayjs";
import request from "../utils/request";

const question = ref("");

const result = ref([]);

const loadState = ref(false);

const clickHandle = () => {
  if (question.value == "") {
    layer.msg("请输入发送的内容", { icon: 2, time: 2000 });
    return false;
  }
  loadState.value = true;
  let t = dayjs().format("YYYY-MM-DD HH:mm:ss");

  result.value.unshift(
    '<pre style="text-align: right">' + t + "\n" + question.value + "</pre>"
  );
  request({
    url: "/",
    method: "post",
    data: { question: question.value },
  }).then((res) => {
    t = dayjs().format("YYYY-MM-DD HH:mm:ss");
    result.value.unshift(
      '<pre style="text-align: left">' + t + "\n" + res.data.message + "</pre>"
    );
    question.value = "";
    loadState.value = false;
  });
};
</script>

<style>
.h-16 {
  height: 100%;
}
.h-16 input {
  background: #fff;
}
.example {
  height: 100%;
  max-width: 400px;
  margin: 0 auto;
}
.example .layui-footer {
  line-height: 36px;
}
.example .layui-header {
  line-height: 60px;
}
.example .layui-footer,
.example .layui-header {
  text-align: center;
  background: #efefef;
  /* color: white; */
}
.example .layui-body {
  align-items: center;
  justify-content: center;
  /* color: white; */
  background-color: rgba(195, 195, 195, 0.5) !important;
}
pre {
  white-space: pre-wrap;
}
</style>