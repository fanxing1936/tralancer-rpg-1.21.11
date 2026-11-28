# 冒险模式：原版合成表全部禁用（world_loot / 用户 2026-11-23）
execute in minecraft:overworld run gamerule limited_crafting true
execute in minecraft:the_nether run gamerule limited_crafting true
execute in minecraft:the_end run gamerule limited_crafting true
execute in rpg:paradise_lost run gamerule limited_crafting true
execute in rpg:daath run gamerule limited_crafting true
execute in rpg:armageddon run gamerule limited_crafting true
execute in rpg:armageddon_2 run gamerule limited_crafting true
execute in rpg:armageddon_3 run gamerule limited_crafting true
execute in rpg:armageddon_4 run gamerule limited_crafting true
scoreboard objectives add rpg_wl_rl dummy
# 默认保留物品栏、生物不破坏地形（用户 2026-11-28）。原版里游戏规则整个存档共用；
# 但服务端（Paper 等）每个维度是单独的世界、各有一份规则，所以每个维度都写一遍（用户 2026-11-28）。
# 只在装上这一版时设一次（#rules 到 2）：之后服主用 /gamerule 改了，重载不会改回来。
scoreboard objectives add rpg_rules dummy
execute unless score #rules rpg_rules matches 2.. in minecraft:overworld run gamerule keep_inventory true
execute unless score #rules rpg_rules matches 2.. in minecraft:overworld run gamerule mob_griefing false
execute unless score #rules rpg_rules matches 2.. in minecraft:the_nether run gamerule keep_inventory true
execute unless score #rules rpg_rules matches 2.. in minecraft:the_nether run gamerule mob_griefing false
execute unless score #rules rpg_rules matches 2.. in minecraft:the_end run gamerule keep_inventory true
execute unless score #rules rpg_rules matches 2.. in minecraft:the_end run gamerule mob_griefing false
execute unless score #rules rpg_rules matches 2.. in rpg:paradise_lost run gamerule keep_inventory true
execute unless score #rules rpg_rules matches 2.. in rpg:paradise_lost run gamerule mob_griefing false
execute unless score #rules rpg_rules matches 2.. in rpg:daath run gamerule keep_inventory true
execute unless score #rules rpg_rules matches 2.. in rpg:daath run gamerule mob_griefing false
execute unless score #rules rpg_rules matches 2.. in rpg:armageddon run gamerule keep_inventory true
execute unless score #rules rpg_rules matches 2.. in rpg:armageddon run gamerule mob_griefing false
execute unless score #rules rpg_rules matches 2.. in rpg:armageddon_2 run gamerule keep_inventory true
execute unless score #rules rpg_rules matches 2.. in rpg:armageddon_2 run gamerule mob_griefing false
execute unless score #rules rpg_rules matches 2.. in rpg:armageddon_3 run gamerule keep_inventory true
execute unless score #rules rpg_rules matches 2.. in rpg:armageddon_3 run gamerule mob_griefing false
execute unless score #rules rpg_rules matches 2.. in rpg:armageddon_4 run gamerule keep_inventory true
execute unless score #rules rpg_rules matches 2.. in rpg:armageddon_4 run gamerule mob_griefing false
scoreboard players set #rules rpg_rules 2
