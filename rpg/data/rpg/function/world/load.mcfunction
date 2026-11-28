# 冒险模式：原版合成表全部禁用（world_loot / 用户 2026-11-23）
gamerule limited_crafting true
scoreboard objectives add rpg_wl_rl dummy
# 默认保留物品栏、生物不破坏地形（用户 2026-11-28）。游戏规则是整个存档共用的，所有维度（主世界、失乐园、达阿特、序章战场……）一起生效。
# 只在装上这一版时设一次（#rules）：之后服主用 /gamerule 改了，重载不会改回来。
scoreboard objectives add rpg_rules dummy
execute unless score #rules rpg_rules matches 1.. run gamerule keep_inventory true
execute unless score #rules rpg_rules matches 1.. run gamerule mob_griefing false
scoreboard players set #rules rpg_rules 1
