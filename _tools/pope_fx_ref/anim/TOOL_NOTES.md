# TOOL_NOTES

- 工具名：内置 `image_gen.imagegen`（调用名 `image_gen__imagegen`）。
- 是否原生支持 GIF：当前公开说明和参数未提供 GIF 或动画输出能力。参数只有 `prompt`、`transparent_background`、`referenced_image_paths`、`num_last_images_to_include`，返回 `image_url` 和可选 `output_hint`；本次使用静态图路径。
- 帧数上限：工具未声明动画帧数上限，也没有时序帧数参数。`num_last_images_to_include` 的上限 5 是参考图片数量，不是动画帧数。静态图内绘制多少序列帧也没有公布硬性上限，本次通过提示词请求 8 帧。
- 透明是否保留：是。设置 `transparent_background=true`；原样复制生成 PNG 后实测为 32 位 ARGB，Alpha 范围 0–255，完全透明像素 1,299,510 个。
- 实际办法：一次生成包含横排 8 个脉动阶段的静态序列图，保存为 `anim/orb_sheet.png`；未制作 GIF，未使用脚本生成或修改逐帧变化。提示词要求 Minecraft Dungeons 风格像素圣光弹、金色外层、白色内核、上下左右四道短光刺、8 帧脉动循环、透明背景、等宽方形单元、8:1 横排画布。实际输出为 2172×724，包含横排 8 个图案，但未满足 8:1 画布及可直接等分的方形帧要求；保留工具原图，未裁切或重排。
