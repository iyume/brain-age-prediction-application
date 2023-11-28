/// <reference types="vite/client" />

// help typescript to import .vue
declare module "*.vue" {
  import type { DefineComponent } from "vue";
  const component: DefineComponent<{}, {}, any>;
  export default component;
}
