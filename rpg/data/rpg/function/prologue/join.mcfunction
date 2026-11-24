# 接一名玩家进序章（as 玩家）
scoreboard players add #next rpg_pr 1
scoreboard players operation @s rpg_pr_id = #next rpg_pr
execute store result storage rpg:pr tmp.id int 1 run scoreboard players get @s rpg_pr_id
# 木桶不在就不动背包（否则清空了也存不住）
execute in rpg:armageddon unless block 32 30 30 minecraft:barrel run return run function rpg:prologue/join_fail
function rpg:prologue/iso/save with storage rpg:pr tmp
execute if score @s rpg_pr_id matches 1 run function rpg:prologue/iso/stash_1
execute if score @s rpg_pr_id matches 2 run function rpg:prologue/iso/stash_2
execute if score @s rpg_pr_id matches 3 run function rpg:prologue/iso/stash_3
execute if score @s rpg_pr_id matches 4 run function rpg:prologue/iso/stash_4
clear @s
effect clear @s
# 序章全程饱和（用户 2026-11-22），不掉饥饿；回程时 iso/restore_m 的 effect clear 会收回
effect give @s minecraft:saturation infinite 0 true
experience set @s 0 levels
experience set @s 0 points
tag @s remove rpg.pr.join
tag @s add rpg.pr
scoreboard players set @s rpg_pr_role 0
gamemode adventure @s
execute in rpg:armageddon run tp @s -15 81 0 -90 0
item replace entity @s weapon.offhand with minecraft:paper[minecraft:death_protection={},minecraft:item_model="rpg:empty",minecraft:custom_data={rpg_pr_guard:1b}]
