# 冷却递减，仅此而已。
#
# 原本这里还会把 rpg_hud 占成蓄力档 —— 那意味着每用一次柱中之力，
# 魔化条就被顶掉整整 15 秒。契约冷却和魔化一样是**持续状态**，
# 现在两者由 rpg:hud/status 并排画在同一行里，谁也不顶谁。
scoreboard players remove @s rpg_pact_cd 1
