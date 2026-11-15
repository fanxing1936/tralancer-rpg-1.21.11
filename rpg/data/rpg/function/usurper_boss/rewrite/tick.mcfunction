# 被改写的玩家（as 玩家）：任一契约冷却被重新设高，就是刚用了契约技能
scoreboard players remove @s rpg_ub_rw 1
execute if score @s rpg_pact_cd > @s rpg_ub_p1 run function rpg:usurper_boss/rewrite/backlash
execute if score @s rpg_pact_cd2 > @s rpg_ub_p2 run function rpg:usurper_boss/rewrite/backlash
execute if score @s rpg_pact_cd3 > @s rpg_ub_p3 run function rpg:usurper_boss/rewrite/backlash
function rpg:usurper_boss/rewrite/sync
scoreboard players operation #m rpg_ub = @s rpg_ub_rw
scoreboard players set #k rpg_ub 20
scoreboard players operation #m rpg_ub %= #k rpg_ub
execute if score #m rpg_ub matches 0 at @s run function rpg:usurper_boss/rewrite/mote
execute if score @s rpg_ub_rw matches ..0 run function rpg:usurper_boss/rewrite/clear
