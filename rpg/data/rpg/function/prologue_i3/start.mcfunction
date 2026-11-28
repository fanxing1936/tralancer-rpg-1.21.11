# 开始序章（管理员；在执行位置 16 格内最多 4 名玩家进入）
execute if score #state rpg_pr_i3 matches 1.. run return run tellraw @s {"text":"[序章] 序章正在进行；先用 /function rpg:prologue_i3/clear 中止。","color":"#E8D9B0"}
execute unless entity @a[tag=rpg.pr.join3] run return run tellraw @s {"text":"[序章] 附近 16 格内没有可以进入序章的玩家。","color":"#E8D9B0"}
execute if score #fight rpg_mk_i3 matches 1 run return run tellraw @s {"text":"[序章] 有一场米迦勒战正在进行；先清场。","color":"#E8D9B0"}
# 下雨、雷暴会把所有维度的天空一起压暗（实测）：序章期间放晴
weather clear 1800s
execute in rpg:armageddon_3 run forceload add -64 -64 63 63
scoreboard players set #state rpg_pr_i3 1
scoreboard players set #t rpg_pr_i3 0
scoreboard players set #next rpg_pr_i3 0
scoreboard players set #built rpg_pr_i3 0
scoreboard players set #bt rpg_pr_i3 0
tellraw @a[tag=rpg.pr.join3] {"text":"[序章] 正在准备战场…… Preparing the battlefield...","color":"#E8D9B0"}
