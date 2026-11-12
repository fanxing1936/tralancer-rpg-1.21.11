# 路西法静态候选 A：部件表

独立 item_display 共 7 个。16 根骨骼只决定层级；合并子骨骼不增加显示实体。

| 部件 | 包含骨骼 | 发光 | 内容 |
|---|---|---|---|
| body | body, root_front_right, root_front_left, root_back_right, root_back_left | 否 | 腐根衣身、四簇下摆根须 |
| head | head, eyes_glow, sprout_left, sprout_right | 仅 eyes_glow 两个元素 light_emission=15 | 兜帽/帽檐、双眼、两簇嫩芽 |
| right_arm | right_arm, cuff_roots_right | 否 | 右袖、外露骨手、袖口根须 |
| left_arm | left_arm, cuff_roots_left | 否 | 左袖、外露骨手、袖口根须 |
| weapon | right_arm | 否 | held=weapon；仅显示载体主手现有蛇矛，不建武器模型 |
| right_leg | right_leg | 否 | 外露骨腿、右靴 |
| left_leg | left_leg | 否 | 外露骨腿、左靴 |

若六簇根须分别成为独立运动部件，总数为13，超过12，因此均合并回对应身体/手臂部件，不安排根须独立摆动。静态单轴倾角只用于造型。

模型缩放 `model_scale=1.0472011589323151`，`seat=2.0`。全身统一+0.5px落地偏移，原骨架相对关节间距不变；含嫩芽高度2.4格，不含手持矛。
